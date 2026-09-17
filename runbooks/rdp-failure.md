# Runbook: Windows RDP Connection Failed

## Symptom
Cannot establish a Remote Desktop (RDP) session to a Windows 
privileged account.

## Troubleshooting steps

1. **Check server is reachable** — ping the target:

ping <target-ip>

2. **Check RDP is enabled** on the target:
   - System Properties → Remote Desktop → confirm "Enable Remote Desktop" is on
3. **Check port 3389 is open**:

Test-NetConnection <target-ip> -Port 3389

4. **Check firewall rules** — Windows Firewall or network firewall 
   blocking inbound RDP.
5. **Check account permissions** — is the account a member of 
   "Remote Desktop Users" or an Administrator?
6. **Check account status** — is the account locked out after failed 
   login attempts?
7. **Check Event Viewer** on the target for RDP-related errors:
   - Event Viewer → Windows Logs → Security (look for logon failures)

## Resolution
Most RDP failures trace to either the firewall blocking port 3389 
or the account lacking Remote Desktop permissions. Verify both, then 
retry the connection.