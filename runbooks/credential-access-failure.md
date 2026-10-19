# Runbook: User Cannot Retrieve Privileged Credential

## Symptom
User reports they cannot read/retrieve a secret from Vault.

## Troubleshooting steps

1. **Check user authentication** — is their Vault token valid/not expired?

   ```bash
   vault token lookup
   ```

2. **Check user's role/policy** — do they have a policy attached?

   ```bash
   vault token lookup -format=json
   ```

3. **Check the policy itself** — does it grant read on the correct path?

   ```bash
   vault policy read <policy-name>
   ```

4. **Check the secret path** — does the path match exactly (typos are common)?

   ```bash
   vault kv list secret/privileged/
   ```

   Note: `list` needs the `list` capability on `secret/metadata/privileged/*`.
   The `analyst` role does not have it, so run this step as `pamadmin1`.

5. **Check account status** — is the account disabled/locked in the system?
6. **Check Vault server status** — is Vault sealed or down?

   ```bash
   vault status
   ```

7. **Check logs** — any audit log entries showing the denied request?

   ```powershell
   python scripts\audit_report.py C:\vault\audit.log --denied-only
   ```

   A `DENIED` row for the user and path confirms a policy problem rather than
   an outage, and shows exactly which path they tried.

## Resolution
Once the root cause is identified (usually a missing/incorrect policy 
binding), update the policy or token and re-test with:

```bash
vault kv get secret/privileged/<account-name>
```
