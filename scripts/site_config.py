"""Small, non-executing reader for the documented one-line environment format."""
from pathlib import Path
import re

def read_env(path):
    values = {}
    for number, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, separator, value = line.partition("=")
        if not separator or not re.fullmatch(r"[A-Z][A-Z0-9_]*", key):
            raise ValueError(f"Invalid environment entry on line {number}")
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        values[key] = value
    return values

def check_values(values):
    missing = [k for k, v in values.items() if not v or "REPLACE_ME" in v or ".invalid" in v]
    if missing:
        raise ValueError("Replace local settings: " + ", ".join(sorted(missing)))
