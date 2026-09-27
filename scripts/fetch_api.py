"""Download only the immutable, checksum-verified public API dependency."""
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]

def main():
    source = json.loads((ROOT / "release/manifest.json").read_text())["api_source"]
    for name, expected in source["files"].items():
        target = ROOT / "vendor/homelab-api" / name
        if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest() == expected["sha256"]:
            print(f"Verified cached API dependency: {name}")
            continue
        if target.exists():
            raise SystemExit(f"Refusing to overwrite changed dependency: {name}; preserve it before retrying")
        url = f"https://raw.githubusercontent.com/{source['repository']}/{source['commit']}/{name}"
        with urllib.request.urlopen(url, timeout=30) as response:
            data = response.read()
        if hashlib.sha256(data).hexdigest() != expected["sha256"]:
            raise SystemExit(f"Checksum mismatch: {name}")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        print(f"Downloaded and verified API dependency: {name}")

if __name__ == "__main__":
    main()
