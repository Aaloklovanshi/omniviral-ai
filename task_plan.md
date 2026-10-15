# Task Plan: Daily Automated Backup & Verification

**Goal:** Run the daily automated backup script (`C:/Users/aalok/omniviral-ai/scripts/backup_manager.py`), archive codebase, SQLite DB, digital products, and video outputs, sync to Google Drive (`G:\My Drive\OmniViral_Backups`), push git commits, verify integrity, and report status.

## Current Phase
Phase 1: Pre-execution checks & environment verification

## Phases
### Phase 1: Pre-Execution Checks
- **Status:** complete
- Check Google Drive mount (`G:\My Drive`) and target folders: Verified accessible.
- Check python execution environment and git status: Python 3.14.7 verified, repo on master.

### Phase 2: Backup Execution
- **Status:** in_progress
- Execute `backup_manager.py` using Python.
- Monitor execution logs and outputs.

### Phase 3: Post-Backup Integrity & GitHub Verification
- **Status:** pending
- Verify local archive integrity and manifest.
- Verify Google Drive copy (`G:\My Drive\OmniViral_Backups` and `Hermes_OmniViral_Master_Backup`).
- Verify GitHub remote push status.

### Phase 4: Final Reporting
- **Status:** pending
- Deliver concise, factual summary of backup status, sizes, components, and verification results.

## Next Step
Run environment and drive check.
