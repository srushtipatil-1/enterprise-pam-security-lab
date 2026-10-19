# Enterprise PAM Security Lab

A hands-on Privileged Access Management (PAM) lab demonstrating core enterprise security operations concepts using free, open-source, and native tools — built as a practical companion to CyberArk PAM platform knowledge.

## Overview

This project simulates real-world PAM workflows: privileged account management, least-privilege enforcement, credential vaulting, password rotation, RBAC, audit logging, and incident troubleshooting. Every concept is mapped back to its CyberArk equivalent in `documentation/cyberark-mapping.md`.

## What this demonstrates

- Privileged Access Management (PAM) concepts and workflows
- Identity & Access Management (IAM) / Role-Based Access Control (RBAC)
- Least-privilege enforcement (Linux sudo, Windows UAC)
- Secrets management and credential vaulting (HashiCorp Vault)
- Automated password rotation (Python)
- Audit logging and evidence collection
- Incident troubleshooting runbooks / SOPs
- Privileged account onboarding workflow

## Tech stack

HashiCorp Vault, Python, PowerShell, Windows, Linux (Ubuntu), Git/GitHub

## Project structure

- `linux/` — Linux privileged account tests
- `windows/` — Windows privileged account tests (UAC elevation)
- `vault/` — Vault setup, secrets, RBAC policies
- `scripts/` — Password rotation automation
- `runbooks/` — Troubleshooting guides (credential access, rotation, SSH, RDP)
- `documentation/` — Onboarding workflow, audit evidence, CyberArk concept mapping
- `screenshots/` — Evidence for every test performed

## Key evidence

- Least privilege enforcement tested on both Linux and Windows
- Vault RBAC policy tested: read allowed, write denied for restricted role
- Password rotation script verified end-to-end (Vault version increment confirmed)
- Full audit trail captured via Vault's file audit device

## Note

This lab uses open-source and native OS tools to simulate PAM operational concepts for learning and demonstration purposes. It is not affiliated with or a substitute for a production CyberArk deployment. See `documentation/cyberark-mapping.md` for the full concept-to-implementation mapping.

## Hardening update — RBAC, least privilege and audit evidence

| Area | What was added | Where |
|---|---|---|
| Reproducible setup | One idempotent script configures audit device, policies, users and AppRole | `vault/setup-rbac.ps1` |
| RBAC | Three roles (analyst / pam-admin / rotation-service) with named identities, plus an 8-case test plan | `vault/policies/`, `vault/rbac-matrix.md` |
| Least privilege (Vault) | Rotation runs as a **write-only** AppRole instead of the root token | `vault/policies/rotation-service-policy.hcl`, `scripts/rotate_password.py` |
| Least privilege (Linux) | Per-command sudo rule instead of full sudo group | `linux/sudoers-svc-operator`, `linux/scoped-sudo-test.md` |
| Secure rotation | CSPRNG passwords, passed via stdin, never printed; JSON-lines rotation history | `scripts/rotate_password.py`, `logs/rotation-history.jsonl` |
| Audit evidence | Audit log → WHO/WHAT/WHEN/RESULT report highlighting denied requests | `scripts/audit_report.py`, `evidence/` |
| SOP | Weekly privileged-access audit review | `documentation/sop-audit-review.md` |
| Persistent mode (optional) | Non-dev server config with init/unseal | `vault/config/vault-lab.hcl` |

### Quick start

```powershell
$env:VAULT_ADDR = "http://127.0.0.1:8200"
vault server -dev                      # separate window (or: vault server -config=vault/config/vault-lab.hcl)
vault login <root-token>
.\vault\setup-rbac.ps1                 # policies, users, AppRole, audit device
python scripts\rotate_password.py      # rotates as AppRole rotation-service
python scripts\audit_report.py C:\vault\audit.log -o evidence\audit-report.md
```

Scope: rotation updates the credential stored in Vault; it does not change the
password on the target OS account.
