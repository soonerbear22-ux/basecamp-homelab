"""Read only explicitly named Docker objects; emit a narrow public inventory.

No container environment, network, mounts, labels, logs or arbitrary names leave
this process. An absent expected container fails the capture instead of replacing
the last complete observation with an incomplete inventory.
"""
import argparse
import json
from pathlib import Path
import re
import subprocess

CONTAINERS = (
    'beszel', 'beszel-agent', 'grafana', 'homelab-api', 'homepage',
    'node-exporter', 'open-terminal', 'open-webui', 'prometheus', 'qdrant',
    'uptime-kuma',
)
POLICIES = {'no', 'always', 'on-failure', 'unless-stopped'}


def encode(value):
    return json.dumps(value, indent=2, sort_keys=True) + '\n'


def validate(value):
    if type(value) is not dict or set(value) != {'schema_version', 'scope', 'containers'}:
        raise ValueError('Unexpected inventory fields')
    if type(value['schema_version']) is not int or value['schema_version'] != 1 or value['scope'] != 'core-services':
        raise ValueError('Unexpected inventory scope')
    rows = value['containers']
    if type(rows) is not dict or set(rows) != set(CONTAINERS):
        raise ValueError('Incomplete or unexpected container set')
    for row in rows.values():
        if type(row) is not dict or set(row) != {'image_id', 'restart_policy'}:
            raise ValueError('Unexpected container fields')
        if type(row['image_id']) is not str or not re.fullmatch(r'sha256:[a-f0-9]{64}', row['image_id']):
            raise ValueError('Invalid image identifier')
        if type(row['restart_policy']) is not str or row['restart_policy'] not in POLICIES:
            raise ValueError('Invalid restart policy')
    return value


def collect(run=subprocess.check_output):
    rows = {}
    for name in CONTAINERS:
        # Docker's formatter projects only these fields before any output is read.
        raw = run(['docker', 'inspect', '--type', 'container', '--format',
                   '{{json .Image}} {{json .HostConfig.RestartPolicy.Name}}', name],
                  stderr=subprocess.DEVNULL, timeout=20).decode().strip()
        parts = raw.split()
        if len(parts) != 2:
            raise ValueError('Unexpected Docker result')
        rows[name] = dict(image_id=json.loads(parts[0]), restart_policy=json.loads(parts[1]))
    return validate(dict(schema_version=1, scope='core-services', containers=rows))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        content = encode(collect())
        args.output.parent.mkdir(parents=True, exist_ok=True)
        if args.output.exists() and args.output.read_text() == content:
            print('Inventory unchanged; no file replacement.')
            return
        temporary = args.output.with_suffix('.tmp')
        temporary.write_text(content, encoding='utf-8', newline='\n')
        temporary.replace(args.output)
        print('Complete allowlisted inventory saved.')
    except Exception:
        # Docker/OS exception details could contain private operational context.
        raise SystemExit('Inventory collection failed; previous output preserved.') from None


if __name__ == '__main__':
    main()
