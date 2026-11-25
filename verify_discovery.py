#!/usr/bin/env python3
"""verify_discovery.py - Public, read-only verifier.
Checks only published GitHub artifacts. Never loads SSM or gate code.
"""
import hashlib, os, shutil, subprocess, sys, tempfile

REPO = "https://github.com/2fastthompson/The-Discovery.git"
TAG = os.environ.get("DISCOVERY_TAG", "v1.1.8-public")
PRIVATE_PATTERNS = ("ssm_agent", "ssm_live", "executor_v", "gate/", "pc_local_ai_kit")

def die(msg, code=1):
    print(f"FAIL: {msg}")
    sys.exit(code)

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    cwd = os.getcwd().lower()
    for p in PRIVATE_PATTERNS:
        if p.lower() in cwd:
            die("Refusing to run inside a path that looks like the private kit.")

    work = tempfile.mkdtemp(prefix="verify_discovery_")
    try:
        print(f"Fetching public tag {TAG} ...")
        subprocess.check_call(
            ["git", "clone", "--depth", "1", "--branch", TAG, REPO, work],
            stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT,
        )
        for root, dirs, files in os.walk(work):
            for name in files + dirs:
                low = name.lower()
                if any(pat.lower() in low for pat in ("ssm_agent", "ssm_live", "executor_v")):
                    die(f"Unexpected private-looking file: {name}")

        sums = os.path.join(work, "SHA256SUMS.txt")
        if not os.path.isfile(sums):
            die("SHA256SUMS.txt missing")

        mismatches = checked = 0
        with open(sums) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split()
                if len(parts) < 2:
                    continue
                expected, rel = parts[0], parts[-1]
                full = os.path.join(work, rel)
                if not os.path.isfile(full):
                    print(f"  MISSING {rel}")
                    mismatches += 1
                    continue
                actual = sha256_file(full)
                checked += 1
                if actual != expected:
                    print(f"  MISMATCH {rel}")
                    mismatches += 1
                else:
                    print(f"  OK {rel}")

        print(f"\nChecked {checked} files, {mismatches} mismatches.")
        if mismatches:
            die("Hash verification failed")
        print("PASS: Public artifacts match published hashes. No private components accessed.")
        return 0
    finally:
        shutil.rmtree(work, ignore_errors=True)
        print("Working directory cleaned.")

if __name__ == "__main__":
    sys.exit(main())