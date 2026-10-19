# Least Privilege Test — Scoped sudo (Linux)

The original test (`least-privilege-test.md`) shows an all-or-nothing model:
`linux-admin` is in the `sudo` group and can run **any** command as root.
This test shows true least privilege: an operator account that can perform
exactly one privileged task and nothing else.

## Setup (Ubuntu VM: PAM-Linux-Lab)

```bash
sudo adduser svc-operator                      # NOT added to the sudo group
sudo install -m 0440 linux/sudoers-svc-operator /etc/sudoers.d/svc-operator
sudo visudo -cf /etc/sudoers.d/svc-operator    # expect: parsed OK
```

## Tests (run as svc-operator: `su - svc-operator`)

| # | Command | Expected | Screenshot |
|---|---|---|---|
| 1 | `sudo -l` | Lists only `systemctl restart ssh` and `systemctl status ssh` | 14-scoped-sudo-list.png |
| 2 | `sudo systemctl restart ssh` | Allowed | 15-scoped-sudo-allowed.png |
| 3 | `sudo systemctl stop ssh` | Denied: "Sorry, user svc-operator is not allowed to execute ..." | 16-scoped-sudo-denied.png |
| 4 | `sudo cat /etc/shadow` | Denied | 16-scoped-sudo-denied.png |

## Audit evidence (run as an admin)

```bash
sudo journalctl _COMM=sudo --since today | grep svc-operator
```

Expected: one line per attempt, including `command not allowed` for tests 3–4.
Screenshot: 17-scoped-sudo-journal.png

## Conclusion

Privilege is granted per command, not per account: `svc-operator` can keep
SSH running but cannot read credential stores or stop services, and every
attempt — allowed or denied — is recorded by the OS.
