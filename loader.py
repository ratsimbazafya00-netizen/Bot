print(">>> LOADER DÉMARRÉ <<<", flush=True)

import json, time, hashlib, os, sys, urllib.request, shutil, base64
from Crypto.Cipher import AES

# ================= CONFIG =================
GITHUB_USER = "ratsimbazafya00-netizen"
REPO_NAME = "Bot"
BRANCH = "main"
LOCAL_VERSION = "1.0.0"

SECRET = b"YTkxZjNjOWUwZjhjMWIyZC4uLg=="

ENC_FILE = "smmkingdom.enc"
EXPECTED_FILES = {"loader.py", "smmkingdom.enc"}

# ================= ANTI DEBUG =================
def anti_debug():
    if sys.gettrace():
        print("⛔ Debug détecté")
        sys.exit(1)

    for m in ("pdb", "pydevd", "trace"):
        if m in sys.modules:
            print("⛔ Outil de debug détecté")
            sys.exit(1)

# ================= ANTI COPY =================
def anti_copy():
    files = set(os.listdir("."))
    if not EXPECTED_FILES.issubset(files):
        print("⛔ Environnement invalide")
        sys.exit(1)

# ================= MACHINE ID =================
def get_machine_id():
    try:
        data = os.popen("uname -a").read().strip()
    except:
        data = os.getenv("COMPUTERNAME", "unknown")
    return hashlib.sha256(data.encode()).hexdigest()

# ================= URLS =================
def version_url():
    return f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/version.json"

def license_url(mid):
    return f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/licenses/{mid}.json"

def update_url():
    return f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/update/smmkingdom.enc"

# ================= NETWORK =================
def fetch_json(url):
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            return json.loads(r.read().decode())
    except:
        return None

# ================= LICENSE =================
def check_license():
    print("🔍 Vérification licence...")

    mid = get_machine_id()
    print("🖥 Machine ID :", mid)

    lic = fetch_json(license_url(mid))
    if not lic:
        print("❌ Licence absente")
        sys.exit(1)

    if lic.get("status") != "active":
        print("❌ Licence désactivée")
        sys.exit(1)

    if time.time() > lic.get("expire", 0):
        print("❌ LICENCE EXPIRÉE")
        sys.exit(1)

    print("✔ LICENCE VALIDE")

# ================= UPDATE =================
def check_update():
    data = fetch_json(version_url())
    if not data:
        print("⚠️ Update non vérifiable")
        return True

    if data["version"] == LOCAL_VERSION:
        print("✔ Version à jour")
        return True

    if data.get("mandatory"):
        print("⬇️ Mise à jour obligatoire...")
        return download_update()

    return True

def download_update():
    try:
        with urllib.request.urlopen(update_url(), timeout=30) as r:
            with open("smmkingdom.enc.new", "wb") as f:
                shutil.copyfileobj(r, f)

        os.replace("smmkingdom.enc.new", ENC_FILE)
        print("✔ Mise à jour installée")
        return True
    except:
        print("❌ Échec mise à jour")
        return False

# ================= RUN ENC =================
def run_enc():
    key = hashlib.sha256(SECRET).digest()

    with open(ENC_FILE, "rb") as f:
        nonce = f.read(16)
        tag = f.read(16)
        code = f.read()

    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    source = cipher.decrypt_and_verify(code, tag)

    exec(source, {"__name__": "__main__"})

# ================= MAIN =================
def main():
    anti_debug()
    anti_copy()
    check_license()

    if not check_update():
        sys.exit(1)

    print("🚀 Accès autorisé")
    run_enc()

if __name__ == "__main__":
    main()
