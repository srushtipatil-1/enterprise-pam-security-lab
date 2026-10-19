# Role: pam-admin — manages privileged credentials, but is NOT root.
# Separation of duties: can list audit devices but cannot disable them,
# and can read policies but cannot rewrite them.

# Full lifecycle of vaulted privileged credentials
path "secret/data/privileged/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

path "secret/metadata/privileged/*" {
  capabilities = ["read", "list", "delete"]
}

path "secret/metadata/privileged" {
  capabilities = ["list"]
}

# Read-only visibility into RBAC configuration
path "sys/policies/acl/*" {
  capabilities = ["read", "list"]
}

# May list audit devices (vault audit list) — may NOT disable them
path "sys/audit" {
  capabilities = ["read", "sudo"]
}
