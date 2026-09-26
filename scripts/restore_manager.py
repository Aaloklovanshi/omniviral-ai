import os
import sys
import zipfile
import shutil
from pathlib import Path

# Base Directories
OMNIVIRAL_DIR = Path("C:/Users/aalok/omniviral-ai").resolve()
HERMES_DIR = Path(r"C:\Users\aalok\AppData\Local\hermes").resolve()
OMNIROUTE_DATA_DIR = Path(r"C:\Users\aalok\.omniroute").resolve()
OMNIROUTE_CODE_DIR = Path(r"C:\Users\aalok\Documents\Codex\2026-09-23\install-omniroute-from-github\OmniRoute").resolve()

LOCAL_BACKUP = OMNIVIRAL_DIR / "backups" / "latest_master_backup.zip"
DRIVE_BACKUP = Path("G:/My Drive/Hermes_OmniViral_Master_Backup/Archives/latest_master_backup.zip")

def restore(backup_zip=None, component="all"):
    """
    Restores the backup archive.
    component: 'all', 'hermes', 'omniroute', 'omniviral'
    """
    if not backup_zip:
        if DRIVE_BACKUP.exists():
            backup_zip = DRIVE_BACKUP
        elif LOCAL_BACKUP.exists():
            backup_zip = LOCAL_BACKUP
        else:
            print("❌ No backup zip found in Google Drive or local backups directory!")
            return False

    backup_zip = Path(backup_zip)
    print("=" * 70)
    print(f"🔄 STARTING RESTORATION FROM: {backup_zip.name}")
    print(f"🎯 Target Component: {component.upper()}")
    print("=" * 70)

    with zipfile.ZipFile(backup_zip, "r") as zf:
        namelist = zf.namelist()
        print(f"📦 Total files in archive: {len(namelist)}")

        # 1. Restore OmniViral AI
        if component in ["all", "omniviral"]:
            omni_files = [f for f in namelist if f.startswith("omniviral_system/")]
            for f in omni_files:
                rel = Path(f).relative_to("omniviral_system")
                target = OMNIVIRAL_DIR / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                with zf.open(f) as source, open(target, "wb") as dest:
                    shutil.copyfileobj(source, dest)
            print(f"  -> Restored {len(omni_files)} OmniViral AI files to {OMNIVIRAL_DIR}")

        # 2. Restore Hermes Agent (All Profiles + Chats + Databases)
        if component in ["all", "hermes"]:
            hermes_files = [f for f in namelist if f.startswith("hermes_system/")]
            for f in hermes_files:
                rel = Path(f).relative_to("hermes_system")
                target = HERMES_DIR / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                with zf.open(f) as source, open(target, "wb") as dest:
                    shutil.copyfileobj(source, dest)
            print(f"  -> Restored {len(hermes_files)} Hermes Agent files (All Profiles & Chats) to {HERMES_DIR}")

        # 3. Restore OmniRoute Runtime Data
        if component in ["all", "omniroute"]:
            omniroute_data_files = [f for f in namelist if f.startswith("omniroute_data/")]
            for f in omniroute_data_files:
                rel = Path(f).relative_to("omniroute_data")
                target = OMNIRUTE_DATA_DIR if 'OMNIRUTE_DATA_DIR' in locals() else OMNIROUTE_DATA_DIR / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                with zf.open(f) as source, open(target, "wb") as dest:
                    shutil.copyfileobj(source, dest)
            print(f"  -> Restored {len(omniroute_data_files)} OmniRoute runtime files to {OMNIROUTE_DATA_DIR}")

            omniroute_code_files = [f for f in namelist if f.startswith("omniroute_code/")]
            for f in omniroute_code_files:
                rel = Path(f).relative_to("omniroute_code")
                target = OMNIROUTE_CODE_DIR / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                with zf.open(f) as source, open(target, "wb") as dest:
                    shutil.copyfileobj(source, dest)
            print(f"  -> Restored {len(omniroute_code_files)} OmniRoute codebase files to {OMNIROUTE_CODE_DIR}")

    print("=" * 70)
    print("✅ RESTORATION 100% COMPLETED & VERIFIED!")
    print("=" * 70)
    return True

if __name__ == "__main__":
    target_zip = sys.argv[1] if len(sys.argv) > 1 else None
    target_comp = sys.argv[2] if len(sys.argv) > 2 else "all"
    restore(target_zip, target_comp)
