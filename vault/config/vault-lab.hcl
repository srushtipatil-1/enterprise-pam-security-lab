# Persistent (non-dev) Vault server config for the lab — Windows paths.
# Unlike `vault server -dev`, data survives restarts and Vault starts SEALED,
# so init/unseal (Shamir key shares) becomes part of the demonstrated workflow.
#
#   vault server -config=vault/config/vault-lab.hcl

storage "file" {
  path = "C:/vault/data"
}

listener "tcp" {
  address     = "127.0.0.1:8200"
  tls_disable = true   # lab only — production would use TLS
}

api_addr      = "http://127.0.0.1:8200"
ui            = true
disable_mlock = true   # required on Windows
