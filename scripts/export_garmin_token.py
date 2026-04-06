#!/usr/bin/env python3
"""
export_garmin_token.py — run this ONCE locally to generate a Garmin OAuth token.

Opens a VISIBLE Chromium browser window and navigates to Garmin Connect.
Log in normally using the browser window (email, password, MFA if prompted).
The script watches the network traffic in the background and automatically
captures the OAuth tokens once sign-in completes — no DevTools required.
The output is a base64-encoded .tar.gz you paste into GitHub Secrets as
GARMIN_TOKENSTORE.

SETUP (one-time, local machine only — not needed in CI):
  pip install playwright garminconnect
  playwright install chromium

Usage:
  python scripts/export_garmin_token.py

  A browser window will open — sign in as you normally would, then come back
  to this terminal.  The token string will be printed when capture is done.
"""

import base64
import io
import json
import os
import sys
import tarfile
import tempfile
import time

# ── Dependency check ──────────────────────────────────────────────────────────
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("playwright not found.  Run:")
    print("  pip install playwright && playwright install chromium")
    sys.exit(1)

# ── Browser login — intercepts OAuth token responses ─────────────────────────
def capture_tokens_via_browser() -> tuple[dict | None, dict | None]:
    """
    Opens a visible Chromium browser, navigates to Garmin Connect, and waits
    for the user to log in manually.  Network responses are intercepted to
    capture (oauth1_token_dict, oauth2_token_dict).  Either may be None if
    not observed before the window is closed.
    """
    print("\nOpening browser — please sign in to Garmin Connect in the window that appears.")
    print("Come back here after you are logged in.\n")

    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            headless=False,
            args=["--window-size=1280,800"],
        )
        context = browser.new_context(viewport={"width": 1280, "height": 800})
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

        page.goto(
            "https://connect.garmin.com/signin/",
            wait_until="domcontentloaded",
            timeout=30_000,
        )

        # Wait up to 3 minutes for the user to log in and the tokens to appear.
        # Close the browser automatically once both tokens are captured.
        print("Waiting for you to log in (up to 3 minutes)…")
        deadline = time.time() + 180
        while time.time() < deadline:
            if oauth2_data is not None:
                print("\nTokens captured — closing browser.")
                break
            try:
                page.wait_for_timeout(500)
            except Exception:
                break  # page/browser was closed by user

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
    oauth1, oauth2 = capture_tokens_via_browser()

    if oauth2 is None:
        print("\nERROR: OAuth2 token was not captured.")
        print("You may not have finished signing in, or the browser was closed early.")
        print("Re-run the script and make sure you complete the full Garmin login.")
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
refresh the access token automatically when it expires.  Tokens typically
last 90 days; re-run this script when the CI sync starts failing again.
""")

if __name__ == "__main__":
    main()
