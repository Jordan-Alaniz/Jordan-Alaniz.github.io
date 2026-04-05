#!/usr/bin/env python3
"""
generate_token.py — run this ONCE on your local machine to create
a Garmin OAuth token, then paste the output into GitHub Secrets as
GARMIN_TOKENSTORE. After that, the GitHub Action never needs your password.

Usage:
  pip install garminconnect
  py scripts/generate_token.py
"""

import base64, json, os, sys, tempfile

try:
    import garminconnect
except ImportError:
    print("Run first:  pip install garminconnect")
    sys.exit(1)

email    = input("Garmin email: ").strip()
password = input("Garmin password: ").strip()

print("\nLogging in…")
client = garminconnect.Garmin(email, password)
client.login()

# Save the token to a temp dir, then read the JSON file
token_dir = tempfile.mkdtemp(prefix="garth_")
client.garth.dump(token_dir)

# Find the oauth2 token file garth wrote
token_file = os.path.join(token_dir, "oauth2_token.json")
if not os.path.exists(token_file):
    # garth may write it as a different name — list what's there
    files = os.listdir(token_dir)
    print(f"Files in token dir: {files}")
    if files:
        token_file = os.path.join(token_dir, files[0])
    else:
        print("ERROR: No token file found.")
        sys.exit(1)

with open(token_file, "rb") as f:
    raw = f.read()

encoded = base64.b64encode(raw).decode()

print("\n" + "="*60)
print("SUCCESS! Copy everything between the lines below.")
print("="*60)
print(encoded)
print("="*60)
print("""
Next steps:
  1. Go to your GitHub repo → Settings → Secrets and variables
     → Actions → New repository secret
  2. Name:  GARMIN_TOKENSTORE
  3. Value: paste the long string above
  4. You can now DELETE the GARMIN_PASSWORD secret if you want.
  5. Re-run the GitHub Action — it will use the token instead.
""")
