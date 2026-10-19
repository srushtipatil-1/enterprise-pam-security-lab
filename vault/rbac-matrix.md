# Vault RBAC Matrix and Test Plan

Extends `rbac-test.md` (one role) to three roles with named identities, so the
audit log can show **who** did something instead of only `root`.

Setup: `vault/setup-rbac.ps1` (reproducible, idempotent).

## Roles

| Role / policy | Identity (auth method) | secret/privileged/* | Policies | Audit devices |
|---|---|---|---|---|
| `analyst` | `analyst1` (userpass) | read | — | — |
| `pam-admin` | `pamadmin1` (userpass) | create, read, update, delete, list | read, list | list only (cannot disable) |
| `rotation-service` | AppRole `rotation-service` | create, update (**write-only**) | — | — |
| `root` | break-glass only | everything | everything | everything |

## Test cases

| # | As | Command | Expected | Screenshot |
|---|---|---|---|---|
| R1 | analyst1 | `vault kv get secret/privileged/linux-admin` | Allowed | 18-rbac-r1.png |
| R2 | analyst1 | `vault kv put secret/privileged/test-account username=t password=x` | 403 permission denied | 19-rbac-r2.png |
| R3 | analyst1 | `vault policy read analyst` | 403 | 20-rbac-r3.png |
| R4 | pamadmin1 | `vault kv put secret/privileged/svc-backup username=svc-backup password=Temp123!` | Allowed | 21-rbac-r4.png |
| R5 | pamadmin1 | `vault audit disable file/` | 403 (separation of duties) | 22-rbac-r5.png |
| R6 | pamadmin1 | `vault policy write analyst vault/policies/analyst-policy.hcl` | 403 | 22-rbac-r5.png |
| R7 | rotation-service | `python scripts/rotate_password.py` | SUCCESS, `"identity": "approle:rotation-service"` | 23-rbac-r7.png |
| R8 | rotation-service token | `vault kv get secret/privileged/linux-admin` | 403 (write-only role) | 24-rbac-r8.png |

Log in as a user: `vault login -method=userpass username=analyst1`
Get a rotation-service token for R8:
`vault write -field=token auth/approle/login role_id=$env:VAULT_ROLE_ID secret_id=$env:VAULT_SECRET_ID`

## Evidence

After running R1–R8:

```powershell
python scripts\audit_report.py C:\vault\audit.log -o evidence\audit-report.md
```

The report's **Denied requests** table should list R2, R3, R5, R6 and R8,
each attributed to the named identity that attempted it.
