
# Runbook: Linux SSH Connection Failed

## Symptom
Cannot establish an SSH session to a Linux privileged account.

## Troubleshooting steps

1. **Check IP address** — is the target host's IP correct and reachable?

ping <target-ip>

2. **Check DNS** — if using a hostname, does it resolve correctly?
3. **Check SSH service is running** on the target:

sudo systemctl status ssh

4. **Check port 22 is open** — test connectivity:

Test-NetConnection <target-ip> -Port 22

5. **Check firewall rules** — is port 22 blocked on the target or 
   network firewall?
6. **Check username** — correct account name being used?
7. **Check authentication method** — password vs SSH key, and whether 
   the account allows the method being used.
8. **Check logs** on the target:

sudo journalctl -u ssh


## Resolution
Most SSH failures are either network/firewall related (port 22 blocked) 
or the SSH service not running. Restart the service if needed:

sudo systemctl restart ssh