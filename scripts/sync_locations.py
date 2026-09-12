#!/usr/bin/env python3
import json
import pathlib
import urllib.request

REMOTE = "https://crudcrud.com/api/b7617c51e90f44d3a676d7c130ecbfb9/locations"
PATH = pathlib.Path("locations.json")


def key_of(row):
    return (
        row.get("lat"),
        row.get("lng"),
        row.get("time"),
        row.get("local_time"),
    )


def clean(row):
    return {
        "lat": row.get("lat"),
        "lng": row.get("lng"),
        "time": row.get("time"),
        "local_time": row.get("local_time"),
        "accuracy": row.get("accuracy"),
    }


def load_remote():
    try:
        with urllib.request.urlopen(REMOTE, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8"))
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
