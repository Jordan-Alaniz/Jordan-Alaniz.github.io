#!/usr/bin/env python3
"""
export_garmin_token.py — run this ONCE locally to generate a Garmin OAuth token.
The output is a base64 string you paste into GitHub Secrets as GARMIN_TOKENSTORE.

Usage:
  py scripts/export_garmin_token.py
"""

import base64
import getpass
import json
import os
import sys
import tempfile

try:
    import garth
except ImportError:
    print("Installing garth...")
    os.system(f"{sys.executable} -m pip install garth")
    import garth

EMAIL    = input("Garmin email: ").strip()
PASSWORD = getpass.getpass("Garmin password: ")

print("\nLogging in to Garmin Connect...")
client = garth.Client()
client.login(EMAIL, PASSWORD)

# Save tokens to a temp dir, then read them back
token_dir = tempfile.mkdtemp(prefix="garth_export_")
client.dump(token_dir)

# Find the oauth2 token file garth wrote
token_file = os.path.join(token_dir, "oauth2_token.json")
if not os.path.exists(token_file):
    # garth may write it as a different name — find whatever is there
    files = os.listdir(token_dir)
    if not files:
        print("ERROR: No token files written. Login may have failed.")
        sys.exit(1)
    token_file = os.path.join(token_dir, files[0])

with open(token_file, "rb") as f:
    token_bytes = f.read()

encoded = base64.b64encode(token_bytes).decode("utf-8")

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
""")
