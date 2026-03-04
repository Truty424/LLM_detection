import re
from pathlib import Path

ENTRYPOINT_MAP = {
    "cipher": "Cipher",
    "chacha20poly1305": "ChaCha20Poly1305",
}

ALGO_CLASS_MAP = {
    "aes": "AES",
    "camellia": "Camellia",
}


def enrich_with_evidence(components, file_path):
    lines = Path(file_path).read_text(encoding="utf-8").splitlines()

    for component in components:
        token_raw = (component.get("additionalContext") or "").strip()
        if not token_raw:
            continue

        # remove '()' if present
        token_raw = re.sub(r"\s*\(\s*\)?\s*$", "", token_raw)

        token = ENTRYPOINT_MAP.get(token_raw.lower(), token_raw)

        # We search for: Token(  or  .Token(
        token_pattern = re.compile(rf"(?:\b{re.escape(token)}\b|\.{re.escape(token)})\s*\(")

        # If the token is "Cipher", build a regex pattern to match the corresponding
        # algorithm class constructor (e.g., ClassName( or algorithms.ClassName().
        algo_pattern = None
        if token == "Cipher":
            algo_name = (component.get("name") or "").strip().lower()
            algo_class = ALGO_CLASS_MAP.get(algo_name)
            if algo_class:
                algo_pattern = re.compile(
                    rf"(?:\balgorithms\.{re.escape(algo_class)}\b|\b{re.escape(algo_class)}\b)\s*\("
                )

        for line_number, line in enumerate(lines, start=1):
            stripped = line.lstrip()
            if stripped.startswith("import ") or stripped.startswith("from "):
                continue

            m = token_pattern.search(line)
            if not m:
                continue

            if algo_pattern and not algo_pattern.search(line):
                continue

            component["evidence"] = {
                "occurrences": [{
                    "location": file_path,
                    "line": line_number,
                    "offset": m.start(),
                    "additionalContext": token,
                }]
            }
            break

    return components
