# CyberArk Concept Mapping

This document maps core CyberArk PAM operational concepts to their equivalent implementation in this lab project, built using open-source and native tools.

## Concept Mapping Table

| CyberArk Concept       | Lab Implementation                          |
|-------------------------|----------------------------------------------|
| Safe                    | Vault secret path structure (secret/privileged/*) |
| Account                 | Linux/Windows privileged account (linux-admin, winadmin) |
| Platform                | Target OS/account type (Linux sudo, Windows Administrator) |
| Policy                  | Vault access policy (analyst-policy.hcl)     |
| Credential management   | HashiCorp Vault (secrets engine)             |
| Password rotation       | Python automation script (rotate_password.py) |
| Session management      | SSH/RDP privileged session concept           |
| Audit                   | Vault file audit device (audit.log)          |
| Account onboarding      | Documented onboarding workflow               |
| Operations/troubleshooting | Runbooks (credential access, rotation, SSH, RDP failures) |
| Least privilege         | UAC elevation (Windows) / sudo group (Linux) |
| RBAC                    | Vault policies (analyst read-only vs root)   |

## Full access lifecycle demonstrated

    User authentication
           |
    Authorization (RBAC policy)
           |
    Privileged access request
           |
    Credential retrieval (Vault)
           |
    Session (SSH/RDP concept)
           |
    Activity logging (audit.log)
           |
    Password rotation (scripted)
           |
    Audit evidence (screenshots + logs)

## Important note

This project uses open-source and native OS tools (HashiCorp Vault, Windows UAC, Linux sudo, Python) to simulate and demonstrate PAM operational concepts. It does not claim to be a production CyberArk deployment. The goal is to demonstrate practical understanding of privileged access management principles that transfer directly to enterprise PAM platforms like CyberArk.

## Skills demonstrated

PAM, IAM, RBAC, least privilege, secrets management, credential vaulting, password rotation, audit logging, troubleshooting, account onboarding, Windows and Linux administration, Python scripting, Git/GitHub version control.