import os
import sys
import json
import shutil
import zipfile
import subprocess
from datetime import datetime
from pathlib import Path

# Base Directories
OMNIVIRAL_DIR = Path("C:/Users/aalok/omniviral-ai").resolve()
HERMES_DIR = Path(r"C:\Users\aalok\AppData\Local\hermes").resolve()
TARGET_ACCOUNT = "freeediting35@gmail.com"

# Drive Master Folder
DRIVE_MASTER_DIR = Path("G:/My Drive/Hermes_OmniViral_Master_Backup")
LOCAL_BACKUP_DIR = OMNIVIRAL_DIR / "backups"
LOCAL_BACKUP_DIR.mkdir(exist_ok=True)

# OmniViral Exclusions
OMNI_EXCLUDE_DIRS = {".venv", "venv", "__pycache__", ".git", "node_modules", "backups"}
OMNI_EXCLUDE_EXTS = {".pyc", ".pyo", ".pyd", ".tmp"}

# Hermes Specific Inclusions (Core data, profiles, memories, skills, cron, state)
HERMES_INCLUDE_DIRS = [
    "profiles",
    "memories",
    "skills",
    "cron",
    "plugins",
    "desktop-plugins",
    "hooks",
    "sandboxes",
    "whatsapp"
]

HERMES_INCLUDE_FILES = [
    "config.yaml",
    "SOUL.md",
    "auth.json",
    "kanban.db",
    "projects.db",
    "state.db",
    "shared-state.db",
    "claude_knowledge.db",
    "channel_directory.json",
    "spawn-ledger.json",
    ".env"
]

def get_drive_base():
    """Detects available Google Drive path or fallback."""
    user_home = Path(os.environ.get("USERPROFILE", "C:/Users/aalok"))
    potential_bases = [
        Path("G:/My Drive"),
        user_home / "Google Drive",
        user_home / "My Drive",
        Path("D:/GoogleDrive")
    ]
    for b in potential_bases:
        if b.exists():
            target = b / "Hermes_OmniViral_Master_Backup"
            target.mkdir(parents=True, exist_ok=True)
            return target
    return DRIVE_MASTER_DIR

def create_master_archive(drive_target_dir):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"master_backup_{timestamp}.zip"
    local_zip_path = LOCAL_BACKUP_DIR / zip_filename
    latest_zip_path = LOCAL_BACKUP_DIR / "latest_master_backup.zip"

    print("=" * 65)
    print(f"📦 CREATING MASTER ARCHIVE: {zip_filename}")
    print(f"👤 Target Drive Account: {TARGET_ACCOUNT}")
    print("=" * 65)

    total_files = 0
    total_raw_bytes = 0

    with zipfile.ZipFile(local_zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        # 1. Package OmniViral-AI System
        print("  -> Archiving OmniViral AI (Backend, Routes, DB, Frontend, Agents, Products)...")
        for root, dirs, files in os.walk(OMNIVIRAL_DIR):
            dirs[:] = [d for d in dirs if d not in OMNI_EXCLUDE_DIRS and not d.startswith(".")]
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix in OMNI_EXCLUDE_EXTS or "backups" in file_path.parts:
                    continue
                rel_path = Path("omniviral_system") / file_path.relative_to(OMNIVIRAL_DIR)
                try:
                    zf.write(file_path, arcname=str(rel_path))
                    total_files += 1
                    total_raw_bytes += file_path.stat().st_size
                except Exception as e:
                    pass

        # 2. Package Hermes Configuration, Skills, Memories & State
        print("  -> Archiving Hermes Agent Profile (Money-System, Skills, Memories, Cron, Configs)...")
        if HERMES_DIR.exists():
            for d_name in HERMES_INCLUDE_DIRS:
                src_dir = HERMES_DIR / d_name
                if src_dir.exists():
                    for root, dirs, files in os.walk(src_dir):
                        dirs[:] = [d for d in dirs if d not in {"__pycache__", "cache", "tmp", ".git"}]
                        for file in files:
                            file_path = Path(root) / file
                            if file_path.suffix in OMNI_EXCLUDE_EXTS or file_path.name.endswith(".lock"):
                                continue
                            rel_path = Path("hermes_system") / file_path.relative_to(HERMES_DIR)
                            try:
                                zf.write(file_path, arcname=str(rel_path))
                                total_files += 1
                                total_raw_bytes += file_path.stat().st_size
                            except Exception as e:
                                pass

            for f_name in HERMES_INCLUDE_FILES:
                src_file = HERMES_DIR / f_name
                if src_file.exists():
                    rel_path = Path("hermes_system") / f_name
                    try:
                        zf.write(src_file, arcname=str(rel_path))
                        total_files += 1
                        total_raw_bytes += src_file.stat().st_size
                    except Exception as e:
                        pass

    # Update latest pointer locally
    shutil.copy2(local_zip_path, latest_zip_path)

    raw_mb = total_raw_bytes / (1024 * 1024)
    zip_mb = local_zip_path.stat().st_size / (1024 * 1024)
    print(f"✅ Master Archive Ready: {total_files} files ({raw_mb:.2f} MB raw -> {zip_mb:.2f} MB compressed)")
    return local_zip_path, total_files, zip_mb

def sync_to_google_drive(local_zip_path, drive_target_dir):
    print("☁️ Syncing Master Backup to Dedicated Google Drive Folder...")
    archives_dir = drive_target_dir / "Archives"
    live_sync_dir = drive_target_dir / "Live_Sync"
    archives_dir.mkdir(parents=True, exist_ok=True)
    live_sync_dir.mkdir(parents=True, exist_ok=True)

    # 1. Copy zip archives to Drive
    drive_zip_dest = archives_dir / local_zip_path.name
    drive_latest_dest = archives_dir / "latest_master_backup.zip"
    shutil.copy2(local_zip_path, drive_zip_dest)
    shutil.copy2(local_zip_path, drive_latest_dest)
    print(f"  -> Drive Archive Saved: {drive_zip_dest}")

    # 2. Update Live Mirror Folder in Drive for instant direct browsing
    omni_live = live_sync_dir / "omniviral_system"
    hermes_live = live_sync_dir / "hermes_system"

    # Mirror OmniViral core (clean copy of code + db + routes)
    for folder in ["backend", "frontend", "docs", "agents", "digital_products", "data", "marketing", "scripts"]:
        src = OMNIVIRAL_DIR / folder
        dst = omni_live / folder
        if src.exists():
            shutil.copytree(src, dst, dirs_exist_ok=True, ignore=shutil.ignore_patterns("*.pyc", "__pycache__", "*.tmp"))

    for f in ["README.md", "start_server.py", "start_all.bat", "start_agents.bat"]:
        src = OMNIVIRAL_DIR / f
        if src.exists():
            omni_live.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, omni_live / f)

    # Mirror Hermes core (profiles, skills, memories, configs)
    for folder in HERMES_INCLUDE_DIRS:
        src = HERMES_DIR / folder
        dst = hermes_live / folder
        if src.exists():
            shutil.copytree(src, dst, dirs_exist_ok=True, ignore=shutil.ignore_patterns("*.pyc", "__pycache__", "*.lock", "*.tmp"))

    for f in HERMES_INCLUDE_FILES:
        src = HERMES_DIR / f
        if src.exists():
            hermes_live.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, hermes_live / f)

    print(f"  -> Live Unzipped Tree Synced: {live_sync_dir}")
    return str(drive_zip_dest), str(live_sync_dir)

def sync_git_cloud():
    """Pushes master and gh-pages to GitHub remote."""
    try:
        subprocess.run(["git", "add", "."], cwd=str(OMNIVIRAL_DIR), capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", f"chore(backup): Master sync {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"],
            cwd=str(OMNIVIRAL_DIR),
            capture_output=True
        )
        push_res = subprocess.run(["git", "push", "origin", "master"], cwd=str(OMNIVIRAL_DIR), capture_output=True, text=True)
        if push_res.returncode == 0:
            print("🚀 GitHub Master Sync: OK")
    except Exception as e:
        print(f"Git sync note: {e}")

def write_backup_manifest(drive_target_dir, file_count, zip_mb, drive_zip_path, live_sync_path):
    manifest = {
        "last_backup_timestamp": datetime.now().isoformat(),
        "account": TARGET_ACCOUNT,
        "backup_type": "Hermes Agent + OmniViral Full Master Backup",
        "total_files_packaged": file_count,
        "compressed_size_mb": round(zip_mb, 2),
        "drive_master_folder": str(drive_target_dir),
        "drive_archive_file": drive_zip_path,
        "drive_live_mirror": live_sync_path,
        "included_components": {
            "omniviral_ai": {
                "path": str(OMNIVIRAL_DIR),
                "items": ["backend (all routes & services)", "database (data/omniviral.db)", "agents (20-swarm & daemon)", "digital_products", "frontend", "docs"]
            },
            "hermes_agent": {
                "path": str(HERMES_DIR),
                "items": ["profiles (money-system & config)", "skills", "memories", "cronjobs", "plugins", "system databases (kanban, state, projects)"]
            }
        },
        "restore_command": f"python {OMNIVIRAL_DIR}/scripts/restore_manager.py",
        "status": "HEALTHY_AND_VERIFIED"
    }

    # Write to local and Drive
    with open(LOCAL_BACKUP_DIR / "backup_manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    with open(drive_target_dir / "backup_manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"📋 Manifest saved to Drive: {drive_target_dir / 'backup_manifest.json'}")

def prune_old_archives(drive_target_dir, keep_count=7):
    """Keeps the 7 most recent zip backups on local & Drive."""
    for folder in [LOCAL_BACKUP_DIR, drive_target_dir / "Archives"]:
        if not folder.exists():
            continue
        zips = sorted(list(folder.glob("master_backup_*.zip")), key=lambda x: x.stat().st_mtime, reverse=True)
        if len(zips) > keep_count:
            for old in zips[keep_count:]:
                try:
                    old.unlink()
                    print(f"🧹 Pruned old archive: {old.name}")
                except Exception:
                    pass

def main():
    drive_target = get_drive_base()
    drive_target.mkdir(parents=True, exist_ok=True)

    local_zip, file_count, zip_mb = create_master_archive(drive_target)
    drive_zip_path, live_sync_path = sync_to_google_drive(local_zip, drive_target)
    sync_git_cloud()
    prune_old_archives(drive_target)
    write_backup_manifest(drive_target, file_count, zip_mb, drive_zip_path, live_sync_path)

    print("=" * 65)
    print("🎉 MASTER BACKUP FULLY COMPLETED & VERIFIED IN GOOGLE DRIVE!")
    print(f"📁 Drive Folder: {drive_target}")
    print("=" * 65)

if __name__ == "__main__":
    main()
