"""Initialize a missing V1 collection without replacing existing data."""
import argparse
import requests
from site_config import read_env

def ensure_collection(base, session=requests):
    url = base.rstrip("/") + "/collections/homelab_knowledge"
    response = session.get(url, timeout=30)
    if response.status_code == 404:
        created = session.put(url, json={"vectors": {"size": 2560, "distance": "Cosine"}}, timeout=30)
        created.raise_for_status()
        return "created"
    response.raise_for_status()
    vectors = response.json()["result"]["config"]["params"]["vectors"]
    if vectors.get("size") != 2560 or vectors.get("distance") != "Cosine":
        raise ValueError("Existing collection is incompatible; no changes made")
    return "verified"

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", required=True)
    args = parser.parse_args()
    values = read_env(args.env_file)
    try:
        result = ensure_collection(values["QDRANT_URL"])
    except Exception as exc:
        raise SystemExit(f"Collection initialization failed ({type(exc).__name__}); inspect privately") from None
    print(f"Collection {result}: 2560 dimensions, Cosine. Existing points were not replaced.")

if __name__ == "__main__":
    main()
