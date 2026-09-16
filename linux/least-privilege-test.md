# Least Privilege Test — Linux

## Setup
- OS: Ubuntu 26.04 LTS (VirtualBox VM: PAM-Linux-Lab)
- Users created:
  - `srushti` — default install user (has sudo by default)
  - `normaluser` — standard, non-privileged user (no sudo group)
  - `linux-admin` — privileged user (added to sudo group)

## Test 1: Non-privileged user denied
Command: `sudo systemctl restart ssh` (as normaluser)
Result: Access denied — "normaluser is not in the sudoers file."
Screenshot: screenshots/02-sudo-denied-normaluser.png

## Test 2: Privileged user allowed
Command: `sudo systemctl restart ssh` (as linux-admin)
Result: Success — service restarted and shown as active.
Screenshot: screenshots/03-sudo-allowed-linuxadmin.png

## Conclusion
Demonstrates least-privilege enforcement: only accounts explicitly 
granted sudo rights can perform privileged operations.