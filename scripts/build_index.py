#!/usr/bin/env python3
"""Genera el index.pb gzip compatible con el esquema de Keiyoushi."""
import gzip
from pathlib import Path
from google.protobuf import json_format
import index_pb2

root = Path(__file__).resolve().parents[1]
index_json = root / "index.json"
index = json_format.Parse(index_json.read_text(encoding="utf-8"), index_pb2.Index())
if not index.name or not index.signingKey:
    raise ValueError("Faltan name o signingKey en index.json")
for ext in index.extensionList.extensions:
    if not ext.packageName or not ext.resources.apkUrl or not ext.resources.iconUrl:
        raise ValueError(f"Extensión incompleta: {ext.packageName or ext.name}")
output = root / "index.pb"
output.write_bytes(gzip.compress(index.SerializeToString(deterministic=True), mtime=0))
print(f"Generado {output.name} ({output.stat().st_size} bytes)")
