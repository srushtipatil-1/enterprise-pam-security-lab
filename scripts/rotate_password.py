"""Rotate privileged account passwords stored in HashiCorp Vault (KV v2).

Security properties (what makes this PAM-grade rather than a demo):
- Passwords come from `secrets` (a CSPRNG), not `random`, and always mix
  lower/upper/digit/symbol characters.
- The new password is handed to the Vault CLI on stdin (`password=-`), so it
  never appears on a command line, in the process list, or in shell history.
- The password is never printed and never written to the rotation log.
- Least privilege: when VAULT_ROLE_ID / VAULT_SECRET_ID are set, the script
  logs in as the AppRole `rotation-service`, whose policy is write-only.
  Otherwise it falls back to whatever VAULT_TOKEN is already set.
- Every attempt is appended as one JSON line to logs/rotation-history.jsonl.

Scope note: this rotates the credential *stored in Vault*. It does not change
the password on the target OS account (a production PAM CPM would do both).

Usage:
    python scripts/rotate_password.py                  # rotates linux-admin
    python scripts/rotate_password.py linux-admin svc-backup --length 24
"""
import argparse
import json
import os
import secrets
import string
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SYMBOLS = "!@#$%^&*"
ALPHABET = string.ascii_letters + string.digits + SYMBOLS
DEFAULT_LOG = Path(__file__).resolve().parent.parent / "logs" / "rotation-history.jsonl"


def generate_password(length=20):
    """Return a CSPRNG password containing every character class."""
    if length < 12:
        raise ValueError("length must be at least 12")
    while True:
        pw = "".join(secrets.choice(ALPHABET) for _ in range(length))
        if (any(c.islower() for c in pw) and any(c.isupper() for c in pw)
                and any(c.isdigit() for c in pw) and any(c in SYMBOLS for c in pw)):
            return pw


def _first_line(text):
    """Collapse Vault's multi-line CLI error into one short log-safe line."""
    lines = [l.strip(" *\t") for l in (text or "").splitlines() if l.strip()]
    return " | ".join(lines)[:300]


def approle_login():
    """Log in as AppRole rotation-service. Returns (env, identity)."""
    env = os.environ.copy()
    role_id, secret_id = env.get("VAULT_ROLE_ID"), env.get("VAULT_SECRET_ID")
    if not (role_id and secret_id):
        return env, "token:VAULT_TOKEN"
    result = subprocess.run(
        ["vault", "write", "-field=token", "auth/approle/login",
         f"role_id={role_id}", "secret_id=-"],
        input=secret_id, capture_output=True, text=True, env=env,
    )
    if result.returncode != 0:
        raise RuntimeError(f"AppRole login failed: {_first_line(result.stderr)}")
    env["VAULT_TOKEN"] = result.stdout.strip()
    return env, "approle:rotation-service"


def rotate_password(account_name, env=None, identity="token:VAULT_TOKEN", length=20):
    vault_path = f"secret/privileged/{account_name}"
    new_password = generate_password(length)

    result = subprocess.run(
        ["vault", "kv", "put", "-format=json", vault_path,
         f"username={account_name}", "password=-"],
        input=new_password, capture_output=True, text=True,
        env=env if env is not None else os.environ.copy(),
    )
    del new_password

    entry = {
        "account": account_name,
        "vault_path": vault_path,
        "rotation_status": "SUCCESS" if result.returncode == 0 else "FAILED",
        "vault_version": None,
        "identity": identity,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    if result.returncode == 0:
        try:
            entry["vault_version"] = json.loads(result.stdout)["data"]["version"]
        except (ValueError, KeyError, TypeError):
            pass
    else:
        entry["error"] = _first_line(result.stderr)
    return entry


def append_log(entry, log_file):
    log_file = Path(log_file)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with log_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Rotate vaulted privileged passwords")
    parser.add_argument("accounts", nargs="*", default=["linux-admin"])
    parser.add_argument("--length", type=int, default=20)
    parser.add_argument("--log-file", default=str(DEFAULT_LOG))
    args = parser.parse_args(argv)

    try:
        env, identity = approle_login()
    except RuntimeError as exc:
        print(json.dumps({"rotation_status": "FAILED", "error": str(exc)}, indent=2))
        return 1

    failures = 0
    for account in args.accounts:
        entry = rotate_password(account, env=env, identity=identity, length=args.length)
        append_log(entry, args.log_file)
        print(json.dumps(entry, indent=2))
        failures += entry["rotation_status"] != "SUCCESS"
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
