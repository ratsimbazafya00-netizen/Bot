print(">>> LOADER DÉMARRÉ <<<", flush=True)

import json
import time
import hashlib
import os
import sys
import base64
import tempfile
import urllib.request
import shutil


GITHUB_USER = "ratsimbazafya00-netizen"
REPO_NAME = "Bot"
BRANCH = "main"
LOCAL_VERSION = "1.0.0"

# ================= VERSION =================
def version_url():
    return f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/version.json"

def update_file_url():
    return f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/update/smmkingdom.enc"
def check_update():
    print("🔎 Vérification des mises à jour...")

    remote = load_remote_version()

    if not remote:
        print("⚠️ Impossible de vérifier les mises à jour")
        return True

    remote_version = remote.get("version")
    mandatory = remote.get("mandatory", False)
    message = remote.get("message", "")

    if remote_version == LOCAL_VERSION:
        print("✔ Version à jour")
        return True

    print("\n🆕 NOUVELLE VERSION DISPONIBLE")
    print("📦 Version actuelle :", LOCAL_VERSION)
    print("📦 Dernière version :", remote_version)
    print("📝", message)

    if mandatory:
        print("⛔ Mise à jour OBLIGATOIRE")

        ok = download_update()
        if not ok:
            print("❌ Mise à jour impossible")
            return False

        print("🔄 Relance du programme requise")
        return True

def download_update():
    print("⬇️ Téléchargement de la mise à jour...")

    url = update_file_url()
    temp_file = "smmkingdom.enc.new"

    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            with open(temp_file, "wb") as out:
                shutil.copyfileobj(response, out)

        # Remplacer l'ancien fichier
        if os.path.exists("smmkingdom.enc"):
            os.remove("smmkingdom.enc")

        os.rename(temp_file, "smmkingdom.enc")

        print("✔ Mise à jour installée avec succès")
        return True

    except Exception as e:
        print("❌ Échec mise à jour :", e)
        return False

# ================= LICENCE =================
def license_url(machine_id):
    return f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/licenses/{machine_id}.json"

def load_remote_version():
    try:
        with urllib.request.urlopen(version_url(), timeout=10) as r:
            data = r.read().decode("utf-8")
            return json.loads(data)
    except:
        return None

def load_remote_license(machine_id):
    url = license_url(machine_id)

    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            data = r.read().decode("utf-8")
            return json.loads(data)
    except Exception:
        return None



LICENSE_FILE = "license.key"
SECRET = "YTkxZjNjOWUwZjhjMWIyZC4uLg=="  # 🔒 secret intégré


# ================= MACHINE ID =================
def get_machine_id():
    data = os.popen("uname -a").read().strip()
    return hashlib.sha256(data.encode()).hexdigest()


def show_machine_id(machine_id):
    print("\n" + "=" * 60, flush=True)
    print("🖥  IDENTIFIANT UNIQUE DE CETTE MACHINE", flush=True)
    print("-" * 60, flush=True)
    print(machine_id, flush=True)
    print("-" * 60, flush=True)
    print("📩 Envoyez cet ID à votre fournisseur pour la licence", flush=True)
    print("=" * 60 + "\n", flush=True)


# ================= LICENSE CHECK =================
def check_license():
    print("🔍 Vérification licence...")

    machine_id = get_machine_id()

    print("\n================================================")
    print("🖥 IDENTIFIANT UNIQUE DE CETTE MACHINE")
    print(machine_id)
    print("📩 Envoyez cet ID à votre fournisseur")
    print("================================================\n")

    lic = load_remote_license(machine_id)

    if not lic:
        print("❌ Aucune licence trouvée pour cette machine")
        sys.exit(1)

    if lic.get("status") != "active":
        print("❌ Licence désactivée par le fournisseur")
        sys.exit(1)

    now = int(time.time())
    expire = int(lic["expire"])

    if now > expire:
        print("❌ LICENCE EXPIRÉE")
        sys.exit(1)

    print("✔ LICENCE VALIDE")


# ================= RUN =================
def run():
    check_license()

    if not check_update():
        print("⛔ Veuillez mettre à jour le programme")
        sys.exit(1)

    print("🚀 Accès autorisé")




if __name__ == "__main__":
    run()
    if not os.path.exists("smmkingdom.enc"):
        print("⚠️ Fichier principal manquant → téléchargement")
        if not download_update():
            sys.exit(1)
    print("🚀 Lancement SMMKINGDOM...")
    os.system("python smmkingdom.enc")
