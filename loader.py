print(">>> LOADER DÉMARRÉ <<<", flush=True)


import json
import time
import hashlib
import os
import sys
import urllib.request
import shutil

# ================= CONFIG GITHUB =================
GITHUB_USER = "ratsimbazafya00-netizen"
REPO_NAME = "Bot"
BRANCH = "main"
LOADER_VERSION = "1.1.0"

LOCAL_VERSION = "1.1.0"

# ================= URLS =================
def version_url():
    return f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/version.json"

def update_file_url():
    return f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/update/smmkingdom.enc"

def license_url(machine_id):
    return f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/licenses/{machine_id}.json"

# ================= MACHINE ID =================
def get_machine_id():
    data = os.popen("uname -a").read().strip()
    return hashlib.sha256(data.encode()).hexdigest()

def show_machine_id(machine_id):
    print("\n" + "=" * 60)
    print("🖥 IDENTIFIANT UNIQUE DE CETTE MACHINE")
    print("-" * 60)
    print(machine_id)
    print("-" * 60)
    print("📩 Envoyez cet ID à votre fournisseur")
    print("=" * 60 + "\n")

# ================= LOAD REMOTE =================
def load_remote_version():
    try:
        with urllib.request.urlopen(version_url(), timeout=10) as r:
            return json.loads(r.read().decode())
    except:
        return None

def load_remote_license(machine_id):
    try:
        with urllib.request.urlopen(license_url(machine_id), timeout=10) as r:
            return json.loads(r.read().decode())
    except:
        return None

# ================= UPDATE BOT =================
def download_update():
    print("⬇️ Téléchargement mise à jour du bot...")
    try:
        with urllib.request.urlopen(update_file_url(), timeout=30) as r:
            with open("smmkingdom.enc.new", "wb") as f:
                shutil.copyfileobj(r, f)

        if os.path.exists("smmkingdom.enc"):
            os.remove("smmkingdom.enc")

        os.rename("smmkingdom.enc.new", "smmkingdom.enc")
        print("✔ Mise à jour installée")
        return True
    except Exception as e:
        print("❌ Erreur mise à jour :", e)
        return False

# ================= LICENSE CHECK =================
def check_license():
    print("🔍 Vérification licence...")
    machine_id = get_machine_id()
    show_machine_id(machine_id)

    lic = load_remote_license(machine_id)

    if not lic:
        print("❌ Aucune licence trouvée")
        sys.exit(1)

    if lic.get("status") != "active":
        print("❌ Licence désactivée")
        sys.exit(1)

    if time.time() > lic.get("expire", 0):
        print("❌ LICENCE EXPIRÉE")
        sys.exit(1)

    print("✔ LICENCE VALIDE")

# ================= VERSION CHECK =================
def check_update():
    print("🔎 Vérification des mises à jour...")

    remote = load_remote_version()

    if not remote:
        print("⚠️ Impossible de vérifier les mises à jour")
        return True

    remote_version = remote.get("version")
    remote_loader_version = remote.get("loader_version")
    mandatory = remote.get("mandatory", False)
    message = remote.get("message", "")

    # 🔒 MISE À JOUR DU LOADER
    if remote_loader_version and remote_loader_version != LOADER_VERSION:
        print("⛔ Mise à jour du loader requise")
        print(f"📦 Loader local : {LOADER_VERSION}")
        print(f"📦 Loader distant : {remote_loader_version}")
        print("➡️ Lancement de la mise à jour...")
        os.system("python update_loader.py")
        sys.exit(0)

    # 🔄 MISE À JOUR DU BOT
    if remote_version == LOCAL_VERSION:
        print("✔ Version du bot à jour")
        return True

    print("\n🆕 NOUVELLE VERSION DISPONIBLE")
    print("📦 Version actuelle :", LOCAL_VERSION)
    print("📦 Dernière version :", remote_version)
    print("📝", message)

    if mandatory:
        print("⛔ Mise à jour OBLIGATOIRE")

        if not download_update():
            print("❌ Mise à jour impossible")
            return False

        print("✔ Mise à jour installée")
        print("🔄 Relance requise")
        return True

    return True


# ================= RUN =================
def run():
    check_license()
    if not check_update():
        sys.exit(1)

    if not os.path.exists("smmkingdom.enc"):
        print("⚠️ Bot manquant → téléchargement")
        if not download_update():
            sys.exit(1)

    print("🚀 Lancement SMMKINGDOM...")
    os.system("python smmkingdom.enc")

if __name__ == "__main__":
    run()




