def build_prompt(filename: str, code: str) -> list[dict]:
    system = """You are a cryptography detector.
Return ONLY plain text.
Do NOT return JSON.
Do NOT return markdown.
Do NOT add explanations.
Detect ONLY cryptographic algorithm assets."""

    user = f"""
Analyze the following file: {filename}

Your task:
Detect every cryptographic algorithm used in the code
and output ONLY the following fields for each finding.

Ignore OID, bom-ref and metadata.

Use EXACTLY this structure for each finding:

COMPONENT
programming language: Python
type: cryptographic-asset
name: <eg. AES>
assetType: <algorithm | certificate | relatedCryptoMaterial | protocol>
primitive: <block-cipher | stream-cipher | hash | mac | kdf | drbg | signature | key-agreement | aead>
parameterSetIdentifier: <key size in bits if inferable, otherwise unknown>
mode: <cbc | ctr | gcm | ecb | none | unknown>
padding: <pkcs7 | oaep | pss | none | unknown>
cryptoFunctions: <comma-separated list from the allowed set; each must be justified by at least one exact substring from CODE>
EVIDENCE
location: file name
additionalContext: <primary crypto API entrypoint>

Rules:
- Output plain text only (no JSON, no markdown, no extra commentary).
- Use lowercase for: primitive, mode, padding, cryptoFunctions.
- If the AES key argument is directly os.urandom(N), parameterSetIdentifier = N*8. Do NOT infer from iv/nonce.
- If no padding concept applies (e.g. CTR), padding = none.
- Padding are only the optional parameter of the cryptographic asset 
- In cryptoFunctions: If encrypt is used, include encrypt. If decrypt is used, include decrypt.
- cryptoFunctions MUST be derived only from explicit method calls present in the source code.
- for assetType take values given from the list <algorithm | certificate | relatedCryptoMaterial | protocol>
- for cryptoFunctions take values given from the list [encrypt| decrypt | sign | verify | derive | generate | wrap | unwrap | mac | key-agreement | hash ]
- If multiple algorithms exist, output multiple COMPONENT blocks.]
- Only create COMPONENT blocks for actual cryptographic algorithms/protocols/certificates used to protect data
- Do not create components for helper classes/modules (padding, encoders, utilities).
- do not take values from the variables name

- Each COMPONENT must include exactly one EVIDENCE block.
- additionalContext must reference the instantiated cryptographic class (primary API object), not a variable, parameter, or generic category.
- additionalContext must match the exact class name that appears in the source code as ClassName() (constructor call).
- Do not create EVIDENCE entries for modes, padding, or helper functions.


CODE:
{code}
""".strip()

    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]
