"""Render only a local Prometheus config; this does not deploy services."""
import argparse
import json
from pathlib import Path
from site_config import read_env, check_values

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", required=True)
    parser.add_argument("--output", default=str(Path(__file__).resolve().parents[1] / "config/prometheus.yml"))
    parser.add_argument("--allow-examples", action="store_true", help="Offline validation only")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    values = read_env(args.env_file)
    if not args.allow_examples:
        check_values(values)
    jobs = [{"job_name": "prometheus", "static_configs": [{"targets": ["localhost:9090"]}]}]
    for job, key in [("core-services", "CORE_NODE_EXPORTER_TARGET"), ("basecamp", "BASECAMP_NODE_EXPORTER_TARGET")]:
        jobs.append({"job_name": job, "static_configs": [{"targets": [values[key]]}]})
    output = Path(args.output)
    if output.exists() and not args.overwrite:
        raise SystemExit("Output exists; review it before using --overwrite")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"global": {"scrape_interval": "15s", "evaluation_interval": "15s"}, "scrape_configs": jobs}, indent=2) + "\n")
    print("Local Prometheus configuration rendered. Private targets are not printed.")

if __name__ == "__main__":
    main()
