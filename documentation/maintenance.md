# Maintenance Operations — Patching, Upgrades, Backups

This document outlines the standard operating procedure for routine maintenance of the PAM environment (Vault in this lab, mirroring CyberArk PVWA/Vault maintenance practices).

## Patching / Upgrade Workflow

1. Review release notes for the new version (check for breaking changes, deprecated features)
2. Check current version:

       vault --version
       vault status

3. Back up current configuration and data before any upgrade (see Backup section below)
4. Test the upgrade in a non-production/lab environment first
5. Schedule a maintenance window (communicate downtime to stakeholders)
6. Stop the running service
7. Replace the binary/package with the new version
8. Restart the service and verify health:

       vault status

9. Run a smoke test — confirm secrets can still be read/written as expected
10. Document the upgrade (version, date, outcome) in the change log

## Backup Workflow

1. Identify what needs backing up:
   - Vault configuration files
   - Policy files (vault/policies/)
   - Audit log files
   - (In production CyberArk: Safe data, Vault database, PVWA config)
2. Copy configuration and policy files to a secure backup location
3. For Vault dev mode specifically: note that data is in-memory only and 
   is lost on restart — in production, persistent storage backends 
   (e.g. file, Consul, Raft) would be backed up on a schedule
4. Verify backup integrity periodically by restoring to a test environment

## Sample maintenance log entry

| Field         | Value                          |
|---------------|--------------------------------|
| Task          | Vault version check            |
| Date          | 2026-09-17                     |
| Performed by  | Srushti Patil                  |
| Version before| N/A (initial install)          |
| Version after | v2.1.1                         |
| Outcome       | Success — service healthy      |

## Why this matters

In a production CyberArk environment, the Operations Support Analyst 
role is responsible for exactly this kind of routine maintenance — 
patching the Vault/PVWA components, verifying backups exist and are 
restorable, and documenting every maintenance action for audit purposes.