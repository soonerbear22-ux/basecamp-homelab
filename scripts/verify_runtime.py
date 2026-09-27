"""Read-only API acceptance check. Output contains aggregate results only."""
import argparse
import json
import urllib.request
from site_config import read_env

PATHS = ["docker/status.json", "host/status.json", "processes/top.json", "history/memory.json", "history/cpu.json", "disk/io.json", "knowledge/search.json?query=workload%20placement&limit=1", "ai-worker/status.json", "knowledge/health.json", "basecamp/status.json", "basecamp/guests.json", "basecamp/storage.json", "audit/full.json"]

def get(base, path):
    with urllib.request.urlopen(base.rstrip("/") + "/" + path, timeout=90) as response:
        return json.load(response)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", required=True)
    parser.add_argument("--expected-points", type=int)
    args = parser.parse_args()
    values = read_env(args.env_file)
    base = values["HOMELAB_API_URL"]
    results = {}; failures = []
    for path in PATHS:
        try:
            results[path] = get(base, path)
        except Exception as exc:
            failures.append({"operation": path.split("?")[0], "error_type": type(exc).__name__})
    health = results.get("knowledge/health.json", {})
    audit = results.get("audit/full.json", {})
    if not health.get("healthy"):
        failures.append({"check": "knowledge health"})
    if health.get("checks", {}).get("embedding", {}).get("dimensions") != 2560:
        failures.append({"check": "embedding dimensions"})
    if not audit.get("complete") or audit.get("components_retrieved") != 7:
        failures.append({"check": "audit completeness"})
    count = health.get("checks", {}).get("qdrant", {}).get("points_count")
    if args.expected_points is not None and count != args.expected_points:
        failures.append({"check": "point count differs from this site's expected baseline"})
    print(json.dumps({"operations_returned_json": len(results), "expected_operations": 13, "knowledge_healthy": health.get("healthy", False), "points": count, "audit_complete": audit.get("complete", False), "failures": failures}, indent=2))
    raise SystemExit(bool(failures))

if __name__ == "__main__":
    main()
