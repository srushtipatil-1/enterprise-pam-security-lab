import random
import string
import subprocess
import json
from datetime import datetime

def generate_password(length=16):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))

def rotate_password(account_name):
    new_password = generate_password()
    vault_path = f"secret/privileged/{account_name}"

    result = subprocess.run(
        ["vault", "kv", "put", vault_path,
         f"username={account_name}",
         f"password={new_password}"],
        capture_output=True, text=True
    )

    timestamp = datetime.now().isoformat()

    if result.returncode == 0:
        status = "SUCCESS"
    else:
        status = "FAILED"

    log_entry = {
        "account": account_name,
        "rotation_status": status,
        "timestamp": timestamp
    }

    print(json.dumps(log_entry, indent=2))
    return log_entry

if __name__ == "__main__":
    rotate_password("linux-admin")