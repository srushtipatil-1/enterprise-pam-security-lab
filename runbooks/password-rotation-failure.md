# Runbook: Password Rotation Failed

## Symptom
The rotation script reports `FAILED` status instead of `SUCCESS`.

## Troubleshooting steps

1. **Check target is reachable** — is Vault server running?

vault status

2. **Check account is active** — does the account still exist in the 
   target system (not deleted/disabled)?
3. **Check authentication** — is the Vault token used by the script 
   still valid?

vault token lookup

4. **Check permissions** — does the token's policy allow `create`/`update` 
   on the secret path (not just `read`)?

vault policy read <policy-name>

5. **Check the script itself** — review error output from the subprocess 
   call for the exact Vault CLI error message.
6. **Check logs** — review the JSON rotation log for the failure timestamp 
   and cross-reference with Vault server logs at that time.

## Resolution
Most rotation failures trace back to either an expired/invalid token 
or a policy that lacks write permissions. Fix the policy binding or 
re-authenticate, then re-run:

python scripts/rotate_password.py

