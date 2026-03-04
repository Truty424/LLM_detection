import re

REQUIRED_FIELDS = [
    "type",
    "name",
    "assetType",
    "primitive",
    # "mode",
    # "padding",
    "cryptoFunctions",
]

OPTIONAL_DEFAULTS = {
    "parameterSetIdentifier": "unknown"
}


def parse_components_from_text(text: str) -> list[dict]:

    # Split by COMPONENT headers (case-insensitive),
    # matching lines that contain only "COMPONENT".
    blocks = re.split(r"\n(?=(?:COMPONENT)\s*$)", text.strip(), flags=re.MULTILINE | re.IGNORECASE)

    components = []

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        first_line = block.splitlines()[0].strip()
        if first_line.lower() != "component":
            continue

        comp = {}
        lines = [l.strip() for l in block.splitlines() if l.strip()]

        for line in lines[1:]:
            if ":" not in line:
                continue

            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()

            if key.lower() == "programming language":
                continue

            key_norm = key  # keep the original field name
            value_norm = value.lower()

            if value_norm in ("none", ""):
                continue

            if key_norm.lower() == "cryptofunctions":
                key_norm = "cryptoFunctions"
                comp[key_norm] = sorted(
                    [v.strip().lower() for v in re.split(r"[,\s]+", value) if v.strip()]
                )
                continue

            if key_norm.lower() == "parametersetidentifier":
                key_norm = "parameterSetIdentifier"
                if value_norm.isdigit():
                    comp[key_norm] = int(value_norm)
                else:
                    comp[key_norm] = "unknown"
                continue

            # Normalize remaining fields,
            # converting values to lowercase for consistency.
            comp[key_norm] = value_norm

        # Fill missing optional fields with default values.
        for k, default in OPTIONAL_DEFAULTS.items():
            if k not in comp:
                comp[k] = default

        missing = [f for f in REQUIRED_FIELDS if f not in comp]
        if missing:
            raise ValueError(f"Missing fields in COMPONENT block: {missing}\n\nBlock:\n{block}")

        components.append(comp)

    return components
