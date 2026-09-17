# Least Privilege Test — Windows

## Setup
- OS: Windows (host machine)
- Test method: PowerShell elevation (UAC) used to demonstrate 
  privileged vs non-privileged execution context

## Test 1: Non-elevated PowerShell denied
Command: `net user testuser3 Test@1234 /add`
Context: Standard (non-elevated) PowerShell session
Result: Access denied — "System error 5 has occurred. Access is denied."
Screenshot: screenshots/04-denied-nonelevated.png

## Test 2: Elevated PowerShell allowed
Command: `net user testuser4 Test@1234 /add`
Context: PowerShell run as Administrator (elevated)
Result: Success — "The command completed successfully."
Screenshot: screenshots/05-allowed-elevated.png

## Conclusion
Demonstrates least-privilege enforcement via Windows UAC: identical 
commands succeed or fail purely based on execution privilege context, 
without requiring separate user account switching.