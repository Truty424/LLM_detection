import sys
import json
from pathlib import Path
from language.python.parser import parse_components_from_text
from engine.detector import detect_crypto_report
from output.cbom_generator import create_cbom_from_components
from language.python.evidence_resolver import enrich_with_evidence

DEFAULT_INPUT = "test/test_pyca_symmetric"
DEFAULT_OUTPUT = "artifacts/crypto_report.txt"
OLLAMA_BASE = "http://localhost:11434"
MODEL = "qwen2.5:7b-instruct"
#MODEL = "qwen2.5-coder:7b"


def iter_py_files(path: Path) -> list[Path]:
    if path.is_dir():
        return sorted(path.rglob("*.py"))
    return [path]


def main():
    in_path = Path(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_INPUT)
    out_file = Path(sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUTPUT)

    py_files = iter_py_files(in_path)
    if not py_files:
        raise SystemExit(f"No .py files found under: {in_path}")

    all_components: list[dict] = []
    all_reports: list[str] = []

    for f in py_files:
        report = detect_crypto_report(
            input_path=str(f),
            ollama_base=OLLAMA_BASE,
            model=MODEL,
            temperature=0,
            timeout=180,
        )

        # optional: for debugging purposes
        all_reports.append(f"\n### FILE: {f}\n{report.strip()}\n")

        # Parse LLM output into validated component dictionaries.
        components = parse_components_from_text(report)

        # scan the source code to find where each component is used
        # and attach evidence (file path, line number, and offset) of the occurrence.
        components = enrich_with_evidence(components, str(f))

        for c in components:
            c.setdefault("sourceFile", str(f))

        all_components.extend(components)

    # optional: for debugging purposes
    out_file.write_text("".join(all_reports), encoding="utf-8")
    print(f"Saved raw LLM reports to: {out_file}")

    # optional: for debugging purposes
    Path("artifacts/crypto_facts.json").write_text(
        json.dumps({"components": all_components}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )
    print(f"Parsed components: {len(all_components)}")
    print("Saved parsed facts to: crypto_facts.json")

    # Build a CBOM from the detected components,
    cbom = create_cbom_from_components(all_components)

    Path("artifacts/cbom.json").write_text(
        json.dumps(cbom, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )
    print("Saved CBOM to: cbom.json")


if __name__ == "__main__":
    main()
