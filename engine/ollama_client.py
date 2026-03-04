import requests


def call_ollama(ollama_base: str, model: str, messages, temperature: float = 0, timeout: int = 180) -> str:

    # 1) /api/chat
    chat_url = f"{ollama_base}/api/chat"
    chat_payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {"temperature": temperature},
    }

    try:
        r = requests.post(chat_url, json=chat_payload, timeout=timeout)
        if r.status_code == 200:
            return r.json()["message"]["content"]
        if r.status_code not in (400, 404):
            raise RuntimeError(f"/api/chat error {r.status_code}: {r.text}")
    except requests.RequestException:
        pass

    # 2) fallback: /api/generate
    gen_url = f"{ollama_base}/api/generate"
    prompt = "\n\n".join([f"{m['role'].upper()}: {m['content']}" for m in messages])
    gen_payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": temperature},
    }

    r2 = requests.post(gen_url, json=gen_payload, timeout=timeout)
    if r2.status_code != 200:
        raise RuntimeError(f"/api/generate error {r2.status_code}: {r2.text}")
    return r2.json()["response"]
