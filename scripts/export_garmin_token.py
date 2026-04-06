#!/usr/bin/env python3
"""
export_garmin_token.py — run this ONCE locally to generate a Garmin OAuth token.
The output is a base64-encoded .tar.gz you paste into GitHub Secrets as
GARMIN_TOKENSTORE.  It stores BOTH the oauth1 and oauth2 token files that
garth needs to refresh expired access tokens automatically in CI.

Usage:
  pip install garth
  python scripts/export_garmin_token.py
"""

import base64
import getpass
import io
import os
import sys
import tarfile
import tempfile

try:
    import garth
except ImportError:
    print("Run first:  pip install garth")
    sys.exit(1)

EMAIL    = input("Garmin email: ").strip()
PASSWORD = getpass.getpass("Garmin password: ")

print("\nLogging in to Garmin Connect...")
client = garth.Client()
client.login(EMAIL, PASSWORD)

# Save ALL token files garth writes (oauth1_token.json + oauth2_token.json)
token_dir = tempfile.mkdtemp(prefix="garth_export_")
client.dump(token_dir)

files = os.listdir(token_dir)
if not files:
    print("ERROR: No token files written. Login may have failed.")
    sys.exit(1)

print(f"Token files saved: {files}")

# Pack the entire token directory into an in-memory .tar.gz
buf = io.BytesIO()
with tarfile.open(fileobj=buf, mode="w:gz") as tar:
    for fname in files:
        fpath = os.path.join(token_dir, fname)
        tar.add(fpath, arcname=fname)
buf.seek(0)
encoded = base64.b64encode(buf.read()).decode("utf-8")

print("\n" + "="*60)
print("SUCCESS! Copy the entire string below (one long line):")
print("="*60)
print(encoded)
print("="*60)
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
