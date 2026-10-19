# Role: rotation-service — machine identity used by scripts/rotate_password.py
# (AppRole auth). Write-only: it can set a new password but can never read
# an existing one, so a leaked rotation token cannot expose credentials.

path "secret/data/privileged/*" {
  capabilities = ["create", "update"]
}
