# Privileged Account Onboarding Workflow

## Process

1. Identify account owner (team/individual responsible)
2. Identify target system (Windows/Linux/application)
3. Determine required privilege level (least privilege principle)
4. Create the account record (this document)
5. Store the credential securely in Vault
6. Apply an access policy (RBAC) scoped to the account's role
7. Test access — confirm the account can perform its intended function
8. Enable monitoring/logging for the account
9. Document the account in this onboarding log

## Sample onboarding record

| Field         | Value              |
|---------------|--------------------|
| Account       | linux-admin        |
| Target System | Ubuntu-01 (lab VM) |
| Owner         | Security Team      |
| Privilege     | Administrator      |
| Environment   | Lab                |
| Rotation      | Enabled (scripted) |
| Monitoring    | Enabled (Vault audit logs) |
| Status        | Active             |
| Onboarded on  | 2026-09-17         |

## Why this matters

This workflow mirrors how enterprise PAM platforms (e.g. CyberArk) 
onboard privileged accounts — ensuring every privileged credential 
has a documented owner, purpose, and lifecycle before it's granted 
access to sensitive systems.