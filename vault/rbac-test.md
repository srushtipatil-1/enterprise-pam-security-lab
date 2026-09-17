# RBAC Test — Vault Policies

## Setup
- Policy created: `analyst` — grants read-only access to `secret/data/privileged/*`
- Policy file: vault/policies/analyst-policy.hcl
- Token generated with analyst policy attached

## Test 1: Analyst reads secret (ALLOWED)
Command: `vault kv get secret/privileged/linux-admin`
Result: Success — returned username and password fields
Screenshot: screenshots/09-rbac-analyst-read-allowed.png

## Test 2: Analyst attempts to write secret (DENIED)
Command: `vault kv put secret/privileged/test-account username="test" password="ShouldFail123!"`
Result: 403 Permission denied — "permission denied"
Screenshot: screenshots/10-rbac-analyst-write-denied.png

## Conclusion
Demonstrates functional RBAC in Vault: a token scoped to the analyst 
policy can read privileged credentials but cannot create or modify 
them, enforcing least privilege at the API level.