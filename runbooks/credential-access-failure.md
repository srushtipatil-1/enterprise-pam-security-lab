# Runbook: User Cannot Retrieve Privileged Credential

## Symptom
User reports they cannot read/retrieve a secret from Vault.

## Troubleshooting steps

1. **Check user authentication** — is their Vault token valid/not expired?
vault token lookup

2. **Check user's role/policy** — do they have a policy attached?

vault token lookup -format=json

3. **Check the policy itself** — does it grant read on the correct path?

vault policy read <policy-name>

4. **Check the secret path** — does the path match exactly (typos are common)?

vault kv list secret/privileged/

5. **Check account status** — is the account disabled/locked in the system?
6. **Check Vault server status** — is Vault sealed or down?

vault status

7. **Check logs** — any audit log entries showing the denied request?

## Resolution
Once the root cause is identified (usually a missing/incorrect policy 
binding), update the policy or token and re-test with:
vault kv get secret/privileged/<account-name>