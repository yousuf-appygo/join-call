#!/usr/bin/env python3
import json
import pathlib
import urllib.request

REMOTE = "https://crudcrud.com/api/0c5e751c477a4f45a8cca37c3c13ea1d/locations"
PATH = pathlib.Path("locations.json")


def key_of(row):
    return (
        row.get("lat"),
        row.get("lng"),
        row.get("time"),
        row.get("local_time"),
    )


def clean(row):
    item = {
        "lat": row.get("lat"),
        "lng": row.get("lng"),
        "time": row.get("time"),
        "local_time": row.get("local_time"),
        "accuracy": row.get("accuracy"),
    }
    return item


def load_remote():
    try:
        with urllib.request.urlopen(REMOTE, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data if isinstance(data, list) else []
    except Exception as exc:
        print("remote fetch failed", exc)
        return []


def load_local():
    if not PATH.exists():
        return []
    return json.loads(PATH.read_text(encoding="utf-8"))


local = load_local()
remote = load_remote()
seen = {}
merged = []
for row in local + remote:
    if row.get("lat") is None or row.get("lng") is None:
        continue
    item = clean(row)
    key = key_of(item)
    if key in seen:
        continue
    seen[key] = True
    merged.append(item)

merged.sort(key=lambda row: str(row.get("time") or ""))
PATH.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")
print("wrote", len(merged), "locations")
