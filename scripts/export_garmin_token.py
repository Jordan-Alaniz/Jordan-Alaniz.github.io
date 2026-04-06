#!/usr/bin/env python3
"""
export_garmin_token.py — run this ONCE locally to generate a Garmin OAuth token.

Uses a headless Chromium browser (via playwright) to submit your credentials to
Garmin's SSO page, bypassing the aggressive rate-limiting Garmin applies to
programmatic HTTP logins.  The browser's network traffic is intercepted to
capture the OAuth1 + OAuth2 tokens that Garmin Connect exchanges after sign-in.
The output is a base64-encoded .tar.gz you paste into GitHub Secrets as
GARMIN_TOKENSTORE.

SETUP (one-time, local machine only — not needed in CI):
  pip install playwright garminconnect
  playwright install chromium

Usage:
  python scripts/export_garmin_token.py

──────────────────────────────────────────────────────────────────────────────
FALLBACK — Manual Token Extraction (no playwright required):

  1. Open https://connect.garmin.com in your browser and sign in normally.
  2. Open DevTools (F12) → Network tab.
  3. In the filter box type "preauthorized".
     Right-click the matching request → Copy → Copy Response.
     Save the text as:  oauth1_token.json
  4. Clear the filter and type "exchange/user/2.0".
     Right-click → Copy → Copy Response.
     Save the text as:  oauth2_token.json
  5. Put both files in a folder (e.g. /tmp/garmin_tokens/), then run:

       python3 - <<'HEREDOC'
       import base64, io, tarfile, os
       d = "/tmp/garmin_tokens"
       buf = io.BytesIO()
       with tarfile.open(fileobj=buf, mode="w:gz") as tar:
           for f in os.listdir(d):
               tar.add(os.path.join(d, f), arcname=f)
       buf.seek(0)
       print(base64.b64encode(buf.read()).decode())
       HEREDOC

  6. Paste the printed string as the GARMIN_TOKENSTORE GitHub secret.
──────────────────────────────────────────────────────────────────────────────
"""

import base64
import getpass
import io
import json
import os
import sys
import tarfile
import tempfile
import time

# ── Dependency check ──────────────────────────────────────────────────────────
try:
    from playwright.sync_api import sync_playwright, TimeoutError as PWTimeoutError
except ImportError:
    print("playwright not found.  Run:")
    print("  pip install playwright && playwright install chromium")
    sys.exit(1)

# ── Interactive prompts ───────────────────────────────────────────────────────
EMAIL    = input("Garmin email: ").strip()
PASSWORD = getpass.getpass("Garmin password: ")

# ── Browser login — intercepts OAuth token responses ─────────────────────────
def login_via_browser(email: str, password: str) -> tuple[dict | None, dict | None]:
    """
    Opens a headless Chromium browser, navigates to Garmin Connect, fills in
    credentials, and returns (oauth1_token_dict, oauth2_token_dict) captured
    from the network responses.  Either value may be None if not intercepted.
    """
    print("\nLaunching headless browser…")

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()

        oauth1_data: dict | None = None
        oauth2_data: dict | None = None

        def on_response(response):
            nonlocal oauth1_data, oauth2_data
            try:
                if response.status != 200:
                    return
                url = response.url
                if "preauthorized" in url:
                    body = response.json()
                    if "oauth_token" in body:
                        oauth1_data = body
                        print("  ✓ Captured OAuth1 token")
                elif "exchange/user/2.0" in url:
                    body = response.json()
                    if "access_token" in body:
                        oauth2_data = body
                        print("  ✓ Captured OAuth2 token")
            except Exception:
                pass

        page.on("response", on_response)

        try:
            print("  Navigating to Garmin Connect…")
            page.goto(
                "https://connect.garmin.com/signin/",
                wait_until="domcontentloaded",
                timeout=30_000,
            )

            print("  Waiting for login form…")
            page.wait_for_selector(
                "#username, input[name='username'], input[type='email']",
                timeout=20_000,
            )

            print("  Filling credentials…")
            page.fill("#username", email)
            page.fill("#password, input[name='password']", password)

            print("  Submitting…")
            page.click("#login-btn-signin, button[type='submit']")

            # Wait up to 30 s for the token exchange to complete
            print("  Waiting for token exchange…")
            deadline = time.time() + 30
            while time.time() < deadline:
                if oauth2_data is not None:
                    break
                page.wait_for_timeout(500)

        except PWTimeoutError as exc:
            print(f"  Browser timeout: {exc}")
        except Exception as exc:
            print(f"  Browser error: {exc}")
        finally:
            browser.close()

    return oauth1_data, oauth2_data

# ── Write garth-compatible token files ───────────────────────────────────────
def write_token_files(token_dir: str, oauth1: dict | None, oauth2: dict) -> None:
    now = time.time()

    if oauth1 is not None:
        oauth1.setdefault("domain", "garmin.com")
        oauth1.setdefault("mfa_token", None)
        oauth1.setdefault("mfa_expiration_timestamp", None)
        with open(os.path.join(token_dir, "oauth1_token.json"), "w") as f:
            json.dump(oauth1, f, indent=2)
        print("  Wrote oauth1_token.json")
    else:
        print("  WARNING: OAuth1 token was not captured.")
        print("           The access token will not be auto-refreshed in CI.")
        print("           Re-run this script or use the manual extraction fallback")
        print("           described at the top of this file.")

    oauth2.setdefault("expires_at", now + oauth2.get("expires_in", 3600))
    if "refresh_token_expires_in" in oauth2:
        oauth2.setdefault(
            "refresh_token_expires_at",
            now + oauth2["refresh_token_expires_in"],
        )
    with open(os.path.join(token_dir, "oauth2_token.json"), "w") as f:
        json.dump(oauth2, f, indent=2)
    print("  Wrote oauth2_token.json")

# ── Main ──────────────────────────────────────────────────────────────────────
def main() -> None:
    oauth1, oauth2 = login_via_browser(EMAIL, PASSWORD)

    if oauth2 is None:
        print("\nERROR: OAuth2 token was not captured.")
        print("Login may have failed, or Garmin changed its authentication flow.")
        print("Try the manual extraction fallback described at the top of this script.")
        sys.exit(1)

    token_dir = tempfile.mkdtemp(prefix="garth_export_")
    print("\nWriting token files…")
    write_token_files(token_dir, oauth1, oauth2)

    files = os.listdir(token_dir)
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        for fname in files:
            fpath = os.path.join(token_dir, fname)
            tar.add(fpath, arcname=fname)
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode("utf-8")

    print("\n" + "=" * 60)
    print("SUCCESS! Copy the entire string below (one long line):")
    print("=" * 60)
    print(encoded)
    print("=" * 60)
    print("""
Next steps:
  1. Go to your GitHub repo → Settings → Secrets and variables → Actions
  2. Click "New repository secret"
  3. Name:  GARMIN_TOKENSTORE
  4. Value: paste the entire string above
  5. Click "Add secret"
  6. Re-run the GitHub Action — it will use the token instead of password login

NOTE: This token encodes BOTH oauth1 and oauth2 credentials so that CI can
refresh the access token automatically when it expires.
""")

if __name__ == "__main__":
    main()
