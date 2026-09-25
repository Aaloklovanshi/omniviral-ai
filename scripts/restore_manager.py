import os
import sys
import zipfile
import shutil
from pathlib import Path

BASE_DIR = Path("C:/Users/aalok/omniviral-ai").resolve()
BACKUP_DIR = BASE_DIR / "backups"
DRIVE_BACKUP = Path("G:/My Drive/OmniViral_Backups/latest_full_backup.zip")

def restore(backup_path=None):
    if not backup_path:
        local_latest = BACKUP_DIR / "latest_full_backup.zip"
        if local_latest.exists():
            backup_path = local_latest
        elif DRIVE_BACKUP.exists():
            backup_path = DRIVE_BACKUP
        else:
            print("❌ No backup zip found in backups/ or Google Drive!")
            return False

    print(f"🔄 Restoring OmniViral AI from: {backup_path}...")
    with zipfile.ZipFile(backup_path, "r") as zf:
        zf.extractall(BASE_DIR)
    print("✅ System successfully restored to state matching backup!")
    return True

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else None
    restore(target)
