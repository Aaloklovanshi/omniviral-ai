# Findings

- Backup script location: `C:/Users/aalok/omniviral-ai/scripts/backup_manager.py`
- Target Drive account: `freeediting35@gmail.com`
- Primary target dirs: `G:/My Drive/OmniViral_Backups`, `G:/My Drive/Hermes_OmniViral_Master_Backup`

## Root Cause Analysis
1. Today's 21:00 scheduled backup failed at line 288 with:
   `OSError: [WinError 1450] Insufficient system resources exist to complete the requested service`
   during `shutil.copy2(local_zip_path, drive_latest_dest)`.
2. Python 3.14 `shutil.copy2` on Windows delegates to `_winapi.CopyFile2()`. For large files (4.55+ GB) against Google Drive virtual filesystem (`G:\`), this exhausts Windows non-paged kernel pool resources when called back-to-back.
3. Fix: Implement a robust buffered copy (`safe_copy_large_file`) with 32MB chunks instead of monolithic `CopyFile2`.
4. Also, for `drive_latest_dest`, copy from `drive_zip_dest` if it already exists, avoiding redundant network/disk transfer, or use `safe_copy_large_file`.
