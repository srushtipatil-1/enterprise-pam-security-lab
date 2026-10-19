# SOP: Privileged Access Audit Review

| Field | Value |
|---|---|
| Owner | Security Operations |
| Frequency | Weekly, and after any incident or RBAC change |
| Inputs | Vault file audit log (`C:\vault\audit.log`), `logs/rotation-history.jsonl`, Linux `journalctl _COMM=sudo` |
| Output | `evidence/audit-report-YYYY-MM-DD.md` committed to the repo |

## Procedure

1. Confirm the audit device is still enabled — an attacker's first move is to turn it off:
   ```powershell
   vault audit list
   ```
   If `file/` is missing: treat as a security incident (step 6).
2. Generate the report:
   ```powershell
   python scripts\audit_report.py C:\vault\audit.log -o evidence\audit-report-$(Get-Date -Format yyyy-MM-dd).md
   ```
3. Review the **Summary**:
   - Root token use should be zero outside documented break-glass or setup.
4. Review **Denied requests**. For each, decide:
   - Expected (test, typo, wrong path) → note it in the report.
   - Unexpected (repeated denials, access to a path outside the user's role) → step 6.
5. Cross-check rotation: every account in `secret/privileged/` should have a
   `SUCCESS` entry in `logs/rotation-history.jsonl` within the rotation period.
   Accounts with `FAILED` → follow `runbooks/password-rotation-failure.md`.
6. Escalate: record time, identity, path and action; revoke the identity's
   tokens (`vault token revoke -accessor <accessor>`) if misuse is suspected.
7. Sign off: add reviewer name, date and outcome at the bottom of the report,
   then commit it to `evidence/`.

## Retention

Raw audit logs stay outside Git (they are covered by `.gitignore` as `*.log`).
Only the generated report, which contains no secret values, is committed.
