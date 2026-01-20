import urllib.request
import shutil
import os
import sys

GITHUB_USER = "ratsimbazafya00-netizen"
REPO = "Bot"
BRANCH = "main"

URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO}/{BRANCH}/loader.py"

print("⬇️ Mise à jour du loader...")

try:
    with urllib.request.urlopen(URL, timeout=30) as r:
        with open("loader.py.new", "wb") as f:
            shutil.copyfileobj(r, f)

    if os.path.exists("loader.py"):
        os.remove("loader.py")

    os.rename("loader.py.new", "loader.py")

    print("✔ Loader mis à jour avec succès")
    print("🔄 Relancez le programme")
except Exception as e:
    print("❌ Échec mise à jour loader :", e)
    sys.exit(1)
