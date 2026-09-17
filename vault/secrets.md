# Vault Secrets Management

## Setup
- HashiCorp Vault v2.1.1 running in dev mode (local, in-memory)
- Address: http://127.0.0.1:8200

## Secret stored
Path: `secret/privileged/linux-admin`
Fields: username, password (fake lab credential — not a real system password)

## Commands used
vault kv put secret/privileged/linux-admin username="linux-admin" password="LabPass123!"
vault kv get secret/privileged/linux-admin

## Result
Secret successfully stored and retrieved, confirming Vault's core 
secrets-management capability — the foundation of PAM-style credential 
vaulting.

Screenshot: screenshots/08-vault-secret-stored-retrieved.png

## Note
Dev mode stores data in memory only — this is for demonstration/learning, 
not production use.