# Password Rotation — Automated Script

## Setup
- Script: scripts/rotate_password.py
- Generates a random 16-character password
- Updates the credential in Vault via CLI subprocess call
- Logs rotation status and timestamp as JSON

## Test 1: Run rotation script
Command: `python scripts/rotate_password.py`
Result: SUCCESS — JSON log printed with timestamp
Screenshot: screenshots/11-password-rotation-success.png

## Test 2: Verify rotation in Vault
Command: `vault kv get secret/privileged/linux-admin`
Result: Password changed from "LabPass123!" (version 1) to a new 
random value (version 2), confirming the rotation actually updated 
the stored credential.
Screenshot: screenshots/12-password-rotation-verified.png

## Conclusion
Demonstrates automated credential lifecycle management — a core PAM 
capability — using Python and the Vault CLI, with audit-friendly 
JSON logging of each rotation event.