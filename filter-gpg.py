#!/usr/bin/env python3
import sys
import subprocess
import tempfile

# Path to the recipient's GPG public key ID or email
RECIPIENT = "ysujaana2004@gmail.com"

def log(msg):
    print(f"filter-gpg: {msg}", file=sys.stderr)

log("starting filter")

message_lines = []

for line in sys.stdin:
    line = line.rstrip("\n")

    if line.startswith("filter-dataline|"):
        payload = line[len("filter-dataline|"):]
        message_lines.append(payload)
        print(line)  # Forward unmodified line
    elif line.startswith("filter-end|"):
        full_message = "\n".join(message_lines)

        try:
            with tempfile.NamedTemporaryFile("w+", delete=False) as temp:
                temp.write(full_message)
                temp.flush()

                result = subprocess.run([
                    "gpg", "--batch", "--yes", "--encrypt", "--armor",
                    "--recipient", RECIPIENT,
                    "--output", temp.name + ".asc",
                    temp.name
                ], capture_output=True)

                if result.returncode != 0:
                    log("encryption failed")
                    log(result.stderr.decode())
                else:
                    log("encryption succeeded")
                    with open(temp.name + ".asc", "r") as f:
                        encrypted = f.read()
                        for line in encrypted.splitlines():
                            print(f"filter-dataline|{line}")

        except Exception as e:
            log(f"error: {e}")

        print("proceed")
    else:
        print("proceed")
