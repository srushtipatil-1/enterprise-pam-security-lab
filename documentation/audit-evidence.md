

# Audit Logging — Vault

## Setup
Enabled Vault's file audit device:

    vault audit enable file file_path=C:\vault\audit.log

## Test
Performed a read operation:

    vault kv get secret/privileged/linux-admin

## Evidence
The audit log captured the full WHO/WHAT/WHEN/RESULT trail:
- WHO: root token (display_name: root)
- WHAT: read operation on path secret/data/privileged/linux-admin
- WHEN: timestamped (ISO 8601 format)
- RESULT: allowed: true

Sensitive fields (username, password) are automatically HMAC-hashed in the audit log by Vault — proving audit logging doesn't leak credentials while still tracking access.

Screenshot: screenshots/13-vault-audit-log.png

## Conclusion
Demonstrates enterprise-grade auditability: every access to a privileged secret is logged with full context, without exposing the secret value itself in the log — matching real PAM platform audit behavior.