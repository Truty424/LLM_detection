from pathlib import Path

from .prompts import build_prompt
from .ollama_client import call_ollama


def detect_crypto_report(
        input_path: str,
        ollama_base: str,
        model: str,
        temperature: float = 0,
        timeout: int = 180,
) -> str:
    code = Path(input_path).read_text(encoding="utf-8")
    messages = build_prompt(Path(input_path).name, code)
    return call_ollama(ollama_base, model, messages, temperature=temperature, timeout=timeout)
