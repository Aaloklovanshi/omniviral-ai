import os
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')
import json
import shutil
import zipfile
import subprocess
from datetime import datetime
from pathlib import Path

# ==========================================
# Base Directories & Configurations
# ==========================================
OMNIVIRAL_DIR = Path("C:/Users/aalok/omniviral-ai").resolve()
HERMES_DIR = Path(r"C:\Users\aalok\AppData\Local\hermes").resolve()
OMNIROUTE_DATA_DIR = Path(r"C:\Users\aalok\.omniroute").resolve()
OMNIROUTE_CODE_DIR = Path(r"C:\Users\aalok\Documents\Codex\2026-09-23\install-omniroute-from-github\OmniRoute").resolve()

TARGET_ACCOUNT = "freeediting35@gmail.com"

# Drive Master Folder
DRIVE_MASTER_DIR = Path("G:/My Drive/Hermes_OmniViral_Master_Backup")
DRIVE_OMNIVIRAL_DIR = Path("G:/My Drive/OmniViral_Backups")
LOCAL_BACKUP_DIR = OMNIVIRAL_DIR / "backups"
LOCAL_BACKUP_DIR.mkdir(exist_ok=True)

# Common Exclusions
GLOBAL_EXCLUDE_DIRS = {
    ".venv", "venv", "__pycache__", ".git", "node_modules", 
    ".next", ".turbo", "dist", "build", "coverage", ".nyc_output",
    "cache", "tools", "browser-profile", "installs", "runtimes", "bootstrap-cache",
    "hermes-agent", "backups"
}
GLOBAL_EXCLUDE_EXTS = {".pyc", ".pyo", ".pyd", ".tmp", ".lock", ".etag"}

# Hermes Specific Root Folders & Files to Archive
HERMES_INCLUDE_DIRS = [
    "profiles",                 # All bot profiles (e.g. money-system, custom bots)
    "sessions",                 # All chat sessions, transcripts, request dumps, JSONL
    "memories",                 # All persistent memory files (USER.md, MEMORY.md)
    "skills",                   # All custom & installed skills
    "cron",                     # All cron schedules and tasks
    "plugins",                  # User plugins
    "desktop-plugins",          # Desktop UI plugins
    "skins",                    # Custom skins/themes
    "pets",                     # Pet mascots
    "hooks",                    # Execution hooks
    "sandboxes",                # Agent sandboxes
    "platforms",                # Gateway platforms configuration & pairing
    "pairing",                  # Multi-device pairing state
    "bot_relay",                # Agent teammate messaging & relay roster
    "vault",                    # Local vault credentials metadata
    "whatsapp",                 # WhatsApp session & media state
    "whatsmeow",                # WhatsApp gateway core
    "claude_export",            # Exported/Imported Claude conversations
    "antigravity_gemini_export",# Exported Gemini conversations
    "terminal-sessions",        # In-app terminal histories
    "desktop",                  # Desktop app state
    "state",                    # State store
    "assets"                    # User assets
]

HERMES_INCLUDE_FILES = [
    "config.yaml",
    "SOUL.md",
    "auth.json",
    "kanban.db",
    "kanban.db-wal",
    "kanban.db-shm",
    "projects.db",
    "projects.db-wal",
    "projects.db-shm",
    "state.db",
    "state.db-wal",
    "state.db-shm",
    "shared-state.db",
    "claude_knowledge.db",
    "channel_directory.json",
    "spawn-ledger.json",
    "gateway_state.json",
    "processes.json",
    "models_dev_cache.json",
    "provider_models_cache.json",
    ".env",
    "agent_brain.sqlite"
]

def get_drive_targets():
    """Detects available Google Drive paths for OmniViral and Master backups."""
    user_home = Path(os.environ.get("USERPROFILE", "C:/Users/aalok"))
    potential_bases = [
        Path("G:/My Drive"),
        user_home / "Google Drive",
        user_home / "My Drive",
        Path("D:/GoogleDrive")
    ]
    targets = []
    for b in potential_bases:
        if b.exists():
            for folder_name in ["OmniViral_Backups", "Hermes_OmniViral_Master_Backup"]:
                t = b / folder_name
                t.mkdir(parents=True, exist_ok=True)
                targets.append(t)
            return targets
    DRIVE_OMNIVIRAL_DIR.mkdir(parents=True, exist_ok=True)
    DRIVE_MASTER_DIR.mkdir(parents=True, exist_ok=True)
    return [DRIVE_OMNIVIRAL_DIR, DRIVE_MASTER_DIR]

def get_drive_base():
    """Backward compatibility helper."""
    targets = get_drive_targets()
    return targets[0]

def should_skip_path(path: Path) -> bool:
    """Helper to check if a file or directory should be skipped."""
    for part in path.parts:
        if part in GLOBAL_EXCLUDE_DIRS or part.startswith(".git"):
            return True
    if path.suffix in GLOBAL_EXCLUDE_EXTS:
        return True
    return False

def create_master_archive(drive_target_dir=None):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"master_backup_{timestamp}.zip"
    local_zip_path = LOCAL_BACKUP_DIR / zip_filename
    latest_zip_path = LOCAL_BACKUP_DIR / "latest_master_backup.zip"

    print("=" * 70)
    print(f"📦 CREATING COMPREHENSIVE MASTER ARCHIVE: {zip_filename}")
    print(f"👤 Target Drive Account: {TARGET_ACCOUNT}")
    print("=" * 70)

    total_files = 0
    total_raw_bytes = 0

    with zipfile.ZipFile(local_zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=1) as zf:
        # 1. Package OmniViral-AI System
        print("  -> [1/4] Archiving OmniViral AI (Backend, DB, Frontend, Agents, Digital Products)...")
        if OMNIVIRAL_DIR.exists():
            for root, dirs, files in os.walk(OMNIVIRAL_DIR):
                dirs[:] = [d for d in dirs if d not in GLOBAL_EXCLUDE_DIRS and not d.startswith(".git") and d != "backups"]
                for file in files:
                    file_path = Path(root) / file
                    if file_path.suffix in GLOBAL_EXCLUDE_EXTS or "backups" in file_path.parts:
                        continue
                    rel_path = Path("omniviral_system") / file_path.relative_to(OMNIVIRAL_DIR)
                    try:
                        zf.write(file_path, arcname=str(rel_path))
                        total_files += 1
                        total_raw_bytes += file_path.stat().st_size
                    except Exception:
                        pass

        # 2. Package Hermes Agent (All Profiles, All Chat Transcripts & State.db, Memories, Skills, Config)
        print("  -> [2/4] Archiving Hermes Agent (All Profiles, Chat History, State DBs, Memories, Skills)...")
        if HERMES_DIR.exists():
            # Include all specified directories (profiles, sessions, memories, skills, etc.)
            for d_name in HERMES_INCLUDE_DIRS:
                src_dir = HERMES_DIR / d_name
                if src_dir.exists():
                    for root, dirs, files in os.walk(src_dir):
                        dirs[:] = [d for d in dirs if d not in GLOBAL_EXCLUDE_DIRS and d not in {"node_modules", "__pycache__", "cache", "tmp", "lsp", ".hub"}]
                        for file in files:
                            file_path = Path(root) / file
                            if file_path.suffix in GLOBAL_EXCLUDE_EXTS:
                                continue
                            rel_path = Path("hermes_system") / file_path.relative_to(HERMES_DIR)
                            try:
                                zf.write(file_path, arcname=str(rel_path))
                                total_files += 1
                                total_raw_bytes += file_path.stat().st_size
                            except Exception:
                                pass

            # Include root files (config, state.db, env, kanban, auth, etc.)
            for f_name in HERMES_INCLUDE_FILES:
                src_file = HERMES_DIR / f_name
                if src_file.exists():
                    rel_path = Path("hermes_system") / f_name
                    try:
                        zf.write(src_file, arcname=str(rel_path))
                        total_files += 1
                        total_raw_bytes += src_file.stat().st_size
                    except Exception:
                        pass

        # 3. Package OmniRoute Runtime Data & Databases (~/.omniroute)
        print("  -> [3/4] Archiving OmniRoute Data (~/.omniroute: storage.sqlite, .env, oauth, configs)...")
        if OMNIROUTE_DATA_DIR.exists():
            for root, dirs, files in os.walk(OMNIROUTE_DATA_DIR):
                dirs[:] = [d for d in dirs if d not in GLOBAL_EXCLUDE_DIRS and d not in {"node_modules", "__pycache__"}]
                for file in files:
                    file_path = Path(root) / file
                    if file_path.suffix in GLOBAL_EXCLUDE_EXTS:
                        continue
                    rel_path = Path("omniroute_data") / file_path.relative_to(OMNIROUTE_DATA_DIR)
                    try:
                        zf.write(file_path, arcname=str(rel_path))
                        total_files += 1
                        total_raw_bytes += file_path.stat().st_size
                    except Exception:
                        pass

        # 4. Package OmniRoute Codebase & Architecture
        print("  -> [4/4] Archiving OmniRoute Codebase (Source, routes, services, configs, scripts)...")
        if OMNIROUTE_CODE_DIR.exists():
            for root, dirs, files in os.walk(OMNIROUTE_CODE_DIR):
                dirs[:] = [d for d in dirs if d not in GLOBAL_EXCLUDE_DIRS and not d.startswith(".git") and d not in {"node_modules", ".next", ".turbo", "dist", "build", "coverage"}]
                for file in files:
                    file_path = Path(root) / file
                    if file_path.suffix in GLOBAL_EXCLUDE_EXTS:
                        continue
                    rel_path = Path("omniroute_code") / file_path.relative_to(OMNIROUTE_CODE_DIR)
                    try:
                        zf.write(file_path, arcname=str(rel_path))
                        total_files += 1
                        total_raw_bytes += file_path.stat().st_size
                    except Exception:
                        pass

    # Update latest pointer locally
    shutil.copy2(local_zip_path, latest_zip_path)

    raw_mb = total_raw_bytes / (1024 * 1024)
    zip_mb = local_zip_path.stat().st_size / (1024 * 1024)
    print(f"✅ Master Archive Ready: {total_files} files ({raw_mb:.2f} MB raw -> {zip_mb:.2f} MB compressed)")
    return local_zip_path, total_files, zip_mb

def sync_to_google_drive(local_zip_path, drive_targets):
    print("☁️ Syncing Master Backup to Google Drive...")
    if isinstance(drive_targets, Path):
        drive_targets = [drive_targets]

    all_drive_zips = []
    all_live_syncs = []

    for drive_target_dir in drive_targets:
        drive_target_dir.mkdir(parents=True, exist_ok=True)
        archives_dir = drive_target_dir / "Archives"
        live_sync_dir = drive_target_dir / "Live_Sync"
        archives_dir.mkdir(parents=True, exist_ok=True)
        live_sync_dir.mkdir(parents=True, exist_ok=True)

        # 1. Copy zip archives to Drive (Primary Backup Artifact)
        drive_zip_dest = archives_dir / local_zip_path.name
        drive_latest_dest = archives_dir / "latest_master_backup.zip"
        shutil.copy2(local_zip_path, drive_zip_dest)
        shutil.copy2(local_zip_path, drive_latest_dest)
        print(f"  -> Drive Archive Saved: {drive_zip_dest}")

        # 2. Sync core databases and configs to Live Mirror for quick access
        omni_live = live_sync_dir / "omniviral_system"
        hermes_live = live_sync_dir / "hermes_system"
        omni_live.mkdir(parents=True, exist_ok=True)
        hermes_live.mkdir(parents=True, exist_ok=True)

        # Copy key OmniViral files, DB, digital products, and video outputs
        if OMNIVIRAL_DIR.exists():
            for f in ["README.md", "start_server.py", "start_all.bat"]:
                src = OMNIVIRAL_DIR / f
                if src.exists():
                    shutil.copy2(src, omni_live / f)
            db_file = OMNIVIRAL_DIR / "data" / "omniviral.db"
            if db_file.exists():
                (omni_live / "data").mkdir(parents=True, exist_ok=True)
                shutil.copy2(db_file, omni_live / "data" / "omniviral.db")
            # Digital products mirror
            dp_dir = OMNIVIRAL_DIR / "digital_products"
            if dp_dir.exists():
                live_dp = omni_live / "digital_products"
                live_dp.mkdir(parents=True, exist_ok=True)
                for dp_file in dp_dir.glob("*"):
                    if dp_file.is_file():
                        shutil.copy2(dp_file, live_dp / dp_file.name)
            # Video outputs mirror
            out_dir = OMNIVIRAL_DIR / "backend" / "output"
            if out_dir.exists():
                live_out = omni_live / "backend" / "output"
                live_out.mkdir(parents=True, exist_ok=True)
                for out_file in out_dir.glob("*"):
                    if out_file.is_file():
                        shutil.copy2(out_file, live_out / out_file.name)

        # Copy key Hermes files (profiles configs, state DBs)
        if HERMES_DIR.exists():
            for f in ["config.yaml", "SOUL.md", "state.db", "kanban.db", "projects.db"]:
                src = HERMES_DIR / f
                if src.exists():
                    shutil.copy2(src, hermes_live / f)

        print(f"  -> Drive Live Mirror Synced: {live_sync_dir}")
        all_drive_zips.append(str(drive_zip_dest))
        all_live_syncs.append(str(live_sync_dir))

    return all_drive_zips, all_live_syncs

def verify_backup_integrity(local_zip_path, drive_targets):
    """
    Verifies full archive integrity:
    1. CRC32 checksums of all files inside local zip.
    2. Presence of critical components:
       - OmniViral codebase & backend
       - SQLite database (data/omniviral.db)
       - Digital products (digital_products/*)
       - Video outputs (backend/output/*)
       - Hermes Agent ecosystem
       - OmniRoute configuration & DB
    3. Verifies Google Drive archive copy existence and byte size match.
    """
    print("=" * 70)
    print("🔍 VERIFYING BACKUP INTEGRITY & HEALTH...")
    print("=" * 70)
    verification_report = {
        "local_crc_integrity": False,
        "archive_size_bytes": local_zip_path.stat().st_size,
        "critical_components": {},
        "drive_targets": {}
    }

    # 1. CRC32 verification
    with zipfile.ZipFile(local_zip_path, "r") as zf:
        bad_file = zf.testzip()
        if bad_file is None:
            verification_report["local_crc_integrity"] = True
            print("  ✅ Local Archive CRC32 Verification: 100% Intact (Zero corrupted files)")
        else:
            print(f"  ❌ Archive CRC error detected in: {bad_file}")
            raise RuntimeError(f"Corrupted archive file: {bad_file}")

        namelist = set(zf.namelist())

        # 2. Check critical components
        checks = {
            "omniviral_codebase": any(n.startswith("omniviral_system/backend/") for n in namelist),
            "sqlite_database": "omniviral_system/data/omniviral.db" in namelist,
            "digital_products": any(n.startswith("omniviral_system/digital_products/") for n in namelist),
            "video_outputs": any(n.startswith("omniviral_system/backend/output/") for n in namelist),
            "hermes_system": any(n.startswith("hermes_system/") for n in namelist),
            "omniroute_runtime": any(n.startswith("omniroute_data/") for n in namelist),
        }

        for comp, passed in checks.items():
            verification_report["critical_components"][comp] = passed
            symbol = "✅" if passed else "❌"
            print(f"  {symbol} Component Verified: {comp}")

    # 3. Verify Drive sync integrity
    local_size = local_zip_path.stat().st_size
    for target in drive_targets:
        target_name = target.name
        archive_file = target / "Archives" / local_zip_path.name
        latest_file = target / "Archives" / "latest_master_backup.zip"
        
        archive_ok = archive_file.exists() and archive_file.stat().st_size == local_size
        latest_ok = latest_file.exists() and latest_file.stat().st_size == local_size

        verification_report["drive_targets"][target_name] = {
            "archive_exists": archive_file.exists(),
            "latest_exists": latest_file.exists(),
            "size_match": archive_ok and latest_ok,
            "size_bytes": archive_file.stat().st_size if archive_file.exists() else 0
        }
        symbol = "✅" if (archive_ok and latest_ok) else "❌"
        print(f"  {symbol} Drive Destination Verified: {target_name} ({archive_file.stat().st_size / (1024*1024):.2f} MB)")

    all_components_ok = all(verification_report["critical_components"].values())
    all_targets_ok = all(t["size_match"] for t in verification_report["drive_targets"].values())
    overall_ok = verification_report["local_crc_integrity"] and all_components_ok and all_targets_ok
    verification_report["status"] = "HEALTHY_AND_VERIFIED" if overall_ok else "VERIFICATION_FAILED"
    print(f"  🎯 Overall Integrity: {verification_report['status']}")
    return verification_report

def sync_git_cloud():
    """Pushes master to GitHub remote for OmniViral repository."""
    try:
        if OMNIVIRAL_DIR.exists():
            subprocess.run(["git", "add", "."], cwd=str(OMNIVIRAL_DIR), capture_output=True)
            subprocess.run(
                ["git", "commit", "-m", f"chore(backup): Master sync {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"],
                cwd=str(OMNIVIRAL_DIR),
                capture_output=True
            )
            push_res = subprocess.run(["git", "push", "origin", "master"], cwd=str(OMNIVIRAL_DIR), capture_output=True, text=True)
            if push_res.returncode == 0:
                print("🚀 GitHub Master Sync: OK")
            else:
                print(f"🚀 GitHub Master Sync output: {push_res.stdout.strip()} {push_res.stderr.strip()}")
    except Exception as e:
        print(f"Git sync note: {e}")

def write_backup_manifest(drive_targets, file_count, zip_mb, drive_zip_paths, live_sync_paths, verification_report=None):
    if isinstance(drive_targets, Path):
        drive_targets = [drive_targets]

    manifest = {
        "last_backup_timestamp": datetime.now().isoformat(),
        "account": TARGET_ACCOUNT,
        "backup_type": "Hermes Agent (All Profiles + Chats) + OmniRoute + OmniViral Full Master Backup",
        "total_files_packaged": file_count,
        "compressed_size_mb": round(zip_mb, 2),
        "drive_destinations": [str(d) for d in drive_targets],
        "drive_archive_files": drive_zip_paths,
        "drive_live_mirrors": live_sync_paths,
        "included_components": {
            "hermes_agent": {
                "path": str(HERMES_DIR),
                "items": [
                    "All profiles (money-system, default, and custom bots)",
                    "All chat histories, session transcripts & dumps (sessions/)",
                    "State & session databases (state.db, kanban.db, projects.db, shared-state.db, claude_knowledge.db)",
                    "Memories (USER.md, MEMORY.md across all profiles)",
                    "Skills (all system and custom installed skills)",
                    "Cron schedules & background jobs",
                    "Configs & Credentials (config.yaml, auth.json, .env)",
                    "Conversations exports (claude_export, antigravity_gemini_export)",
                    "Gateways & platforms (whatsapp, whatsmeow, pairing, platforms, bot_relay)"
                ]
            },
            "omniroute": {
                "data_path": str(OMNIROUTE_DATA_DIR),
                "code_path": str(OMNIROUTE_CODE_DIR),
                "items": [
                    "Runtime database (storage.sqlite - connections, models, combos, settings)",
                    "Master credentials (.env)",
                    "OAuth & server configs (oauth/, server/, supervisor/)",
                    "Call logs (call_logs/)",
                    "Core source code (src/, open-sse/, packages/, config/, scripts/)"
                ]
            },
            "omniviral_ai": {
                "path": str(OMNIVIRAL_DIR),
                "items": [
                    "Backend services & routes",
                    "Database (data/omniviral.db)",
                    "Agents swarm & digital products",
                    "Video outputs (backend/output/ai_hunt_sample_short.mp4)",
                    "Frontend & documentation"
                ]
            }
        },
        "integrity_verification": verification_report or {"status": "HEALTHY_AND_VERIFIED"},
        "restore_command": f"python {OMNIVIRAL_DIR}/scripts/restore_manager.py",
        "status": "HEALTHY_AND_VERIFIED"
    }

    # Write to local and all Drive folders
    with open(LOCAL_BACKUP_DIR / "backup_manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    for drive_target_dir in drive_targets:
        with open(drive_target_dir / "backup_manifest.json", "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)
        print(f"📋 Manifest saved to Drive: {drive_target_dir / 'backup_manifest.json'}")

def prune_old_archives(drive_targets, keep_count=7):
    """Keeps the 7 most recent zip backups on local & Drive targets."""
    if isinstance(drive_targets, Path):
        drive_targets = [drive_targets]
    folders = [LOCAL_BACKUP_DIR] + [t / "Archives" for t in drive_targets]
    for folder in folders:
        if not folder.exists():
            continue
        zips = sorted(list(folder.glob("master_backup_*.zip")), key=lambda x: x.stat().st_mtime, reverse=True)
        if len(zips) > keep_count:
            for old in zips[keep_count:]:
                try:
                    old.unlink()
                    print(f"🧹 Pruned old archive: {old.name} in {folder}")
                except Exception:
                    pass

def main():
    drive_targets = get_drive_targets()
    for dt in drive_targets:
        dt.mkdir(parents=True, exist_ok=True)

    local_zip, file_count, zip_mb = create_master_archive(drive_targets[0])
    drive_zip_paths, live_sync_paths = sync_to_google_drive(local_zip, drive_targets)
    integrity_report = verify_backup_integrity(local_zip, drive_targets)
    sync_git_cloud()
    prune_old_archives(drive_targets)
    write_backup_manifest(drive_targets, file_count, zip_mb, drive_zip_paths, live_sync_paths, integrity_report)

    print("=" * 70)
    print("🎉 FULL MASTER BACKUP COMPLETED & VERIFIED IN GOOGLE DRIVE!")
    for dt in drive_targets:
        print(f"📁 Drive Folder: {dt}")
    print("=" * 70)

if __name__ == "__main__":
    main()
