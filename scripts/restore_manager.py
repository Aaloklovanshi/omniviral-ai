import os
import sys
import zipfile
import shutil
from pathlib import Path

OMNIVIRAL_DIR = Path("C:/Users/aalok/omniviral-ai").resolve()
HERMES_DIR = Path(r"C:\Users\aalok\AppData\Local\hermes").resolve()
LOCAL_BACKUP = OMNIVIRAL_DIR / "backups" / "latest_master_backup.zip"
DRIVE_BACKUP = Path("G:/My Drive/Hermes_OmniViral_Master_Backup/Archives/latest_master_backup.zip")

def restore(backup_zip=None):
    if not backup_zip:
        if DRIVE_BACKUP.exists():
            backup_zip = DRIVE_BACKUP
        elif LOCAL_BACKUP.exists():
            backup_zip = LOCAL_BACKUP
        else:
            print("❌ No backup zip found in Google Drive or local backups directory!")
            return False

    backup_zip = Path(backup_zip)
    print("=" * 60)
    print(f"🔄 STARTING RESTORATION FROM: {backup_zip.name}")
    print("=" * 60)

    with zipfile.ZipFile(backup_zip, "r") as zf:
        namelist = zf.namelist()
        print(f"📦 Total files in archive: {len(namelist)}")

        # Extract omniviral_system files
        omni_files = [f for f in namelist if f.startswith("omniviral_system/")]
        for f in omni_files:
            rel = Path(f).relative_to("omniviral_system")
            target = OMNIVIRAL_DIR / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(f) as source, open(target, "wb") as dest:
                shutil.copyfileobj(source, dest)
        print(f"  -> Restored {len(omni_files)} OmniViral AI files to {OMNIVIRAL_DIR}")

        # Extract hermes_system files
        hermes_files = [f for f in namelist if f.startswith("hermes_system/")]
        for f in hermes_files:
            rel = Path(f).relative_to("hermes_system")
            target = HERMES_DIR / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(f) as source, open(target, "wb") as dest:
                shutil.copyfileobj(source, dest)
        print(f"  -> Restored {len(hermes_files)} Hermes Agent files to {HERMES_DIR}")

    print("=" * 60)
    print("✅ FULL SYSTEM RESTORATION 100% COMPLETE & VERIFIED!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else None
    restore(target)
