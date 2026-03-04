import uuid
from datetime import datetime, timezone
from typing import Any
from enricher.oid import to_oid


def iso_utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _ensure_str(x: Any) -> str:
    if x is None:
        return "unknown"
    return str(x)


def create_cbom_from_components(components: list[dict]) -> dict:

    cbom_components: list[dict] = []

    for c in components:
        algo_props = {
            "primitive": c.get("primitive"),
            "parameterSetIdentifier": _ensure_str(c.get("parameterSetIdentifier")),
            "mode": c.get("mode"),
            "padding": c.get("padding"),
            "cryptoFunctions": c.get("cryptoFunctions", ""),
        }

        algo_props = {k: v for k, v in algo_props.items() if v not in (None, "", [], "unknown")}

        comp_obj: dict = {
            "type": c.get("type"),
            "bom-ref": str(uuid.uuid4()),
            "name": c.get("name"),
            **({"evidence": c["evidence"]} if c.get("evidence") else {}),
            "cryptoProperties": {
                "assetType": c.get("assetType"),
                "algorithmProperties": algo_props,
                "oid": to_oid(c),
            },
        }

        cbom_components.append(comp_obj)

    return {
        "bomFormat": "CycloneDX",
        "specVersion": "1.6",
        "serialNumber": f"urn:uuid:{uuid.uuid4()}",
        "version": 1,
        "metadata": {"timestamp": iso_utc_now()},
        "components": cbom_components,
        "dependencies": [],
    }
