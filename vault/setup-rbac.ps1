<#
.SYNOPSIS
  Reproducible RBAC + audit setup for the Enterprise PAM Security Lab.

.DESCRIPTION
  Run once, as root/admin, against a running and unsealed Vault.
  Safe to re-run: existing mounts, auth methods and audit devices are skipped.

  Creates:
    Policies  : analyst (existing file), pam-admin, rotation-service
    Humans    : userpass users analyst1 (analyst) and pamadmin1 (pam-admin)
    Machine   : AppRole "rotation-service" for scripts/rotate_password.py
    Audit     : file audit device at C:\vault\audit.log
    Seed data : secret/privileged/linux-admin (only if it does not exist)

.EXAMPLE
  $env:VAULT_ADDR = "http://127.0.0.1:8200"
  vault login            # with the root token
  .\vault\setup-rbac.ps1
#>

$ErrorActionPreference = "Stop"
if (-not $env:VAULT_ADDR) { $env:VAULT_ADDR = "http://127.0.0.1:8200" }
$RepoRoot   = Split-Path -Parent $PSScriptRoot
$PolicyDir  = Join-Path $PSScriptRoot "policies"
$AuditPath  = "C:\vault\audit.log"

function Invoke-Vault {
    param([Parameter(ValueFromRemainingArguments = $true)] [string[]] $VaultArgs)
    $out = & vault @VaultArgs
    if ($LASTEXITCODE -ne 0) { throw "vault $($VaultArgs -join ' ') failed (exit $LASTEXITCODE)" }
    return $out
}

function Read-LabPassword([string] $User) {
    $secure = Read-Host "Set a lab password for Vault user '$User'" -AsSecureString
    return [System.Net.NetworkCredential]::new("", $secure).Password
}

Write-Host "== 1. Checking Vault is reachable and unsealed" -ForegroundColor Cyan
Invoke-Vault status | Out-Null

Write-Host "== 2. KV v2 secrets engine at secret/" -ForegroundColor Cyan
$mounts = Invoke-Vault secrets list -format=json | ConvertFrom-Json
if (-not $mounts.'secret/') {
    Invoke-Vault secrets enable -path=secret kv-v2 | Out-Null
    Write-Host "   enabled kv-v2 at secret/"
} else { Write-Host "   already enabled (dev mode does this automatically)" }

Write-Host "== 3. Audit device (enabled BEFORE any user activity)" -ForegroundColor Cyan
try { $audits = Invoke-Vault audit list -format=json | ConvertFrom-Json } catch { $audits = $null }
if (-not $audits -or -not $audits.'file/') {
    New-Item -ItemType Directory -Force -Path (Split-Path $AuditPath) | Out-Null
    Invoke-Vault audit enable file "file_path=$AuditPath" | Out-Null
    Write-Host "   file audit device -> $AuditPath"
} else { Write-Host "   file audit device already enabled" }

Write-Host "== 4. RBAC policies" -ForegroundColor Cyan
Invoke-Vault policy write analyst          (Join-Path $PolicyDir "analyst-policy.hcl")          | Out-Null
Invoke-Vault policy write pam-admin        (Join-Path $PolicyDir "pam-admin-policy.hcl")        | Out-Null
Invoke-Vault policy write rotation-service (Join-Path $PolicyDir "rotation-service-policy.hcl") | Out-Null
Write-Host "   analyst, pam-admin, rotation-service written"

Write-Host "== 5. Human identities (userpass) - named users, not shared root" -ForegroundColor Cyan
$auths = Invoke-Vault auth list -format=json | ConvertFrom-Json
if (-not $auths.'userpass/') { Invoke-Vault auth enable userpass | Out-Null }
$pw = Read-LabPassword "analyst1"
Invoke-Vault write auth/userpass/users/analyst1 "password=$pw" token_policies=analyst token_ttl=1h token_max_ttl=4h | Out-Null
$pw = Read-LabPassword "pamadmin1"
Invoke-Vault write auth/userpass/users/pamadmin1 "password=$pw" token_policies=pam-admin token_ttl=1h token_max_ttl=4h | Out-Null
Remove-Variable pw
Write-Host "   analyst1 -> analyst, pamadmin1 -> pam-admin"

Write-Host "== 6. Machine identity (AppRole) for password rotation" -ForegroundColor Cyan
if (-not $auths.'approle/') { Invoke-Vault auth enable approle | Out-Null }
Invoke-Vault write auth/approle/role/rotation-service `
    token_policies=rotation-service token_ttl=15m token_max_ttl=30m `
    secret_id_ttl=24h secret_id_num_uses=20 | Out-Null
$env:VAULT_ROLE_ID   = Invoke-Vault read  -field=role_id   auth/approle/role/rotation-service/role-id
$env:VAULT_SECRET_ID = Invoke-Vault write -field=secret_id -f auth/approle/role/rotation-service/secret-id
Write-Host "   VAULT_ROLE_ID / VAULT_SECRET_ID set for THIS PowerShell session only (not saved to disk)"

Write-Host "== 7. Seed privileged credential (if missing)" -ForegroundColor Cyan
& vault kv get secret/privileged/linux-admin *> $null
if ($LASTEXITCODE -ne 0) {
    Invoke-Vault kv put secret/privileged/linux-admin username=linux-admin "password=LabPass123!" | Out-Null
    Write-Host "   seeded secret/privileged/linux-admin (rotate it next)"
} else { Write-Host "   secret/privileged/linux-admin already exists" }

Write-Host "`nDone. Verify with:" -ForegroundColor Green
Write-Host "   vault policy list ; vault auth list ; vault audit list"
Write-Host "   python scripts\rotate_password.py      # runs as AppRole rotation-service"
