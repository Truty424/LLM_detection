from __future__ import annotations
from typing import Mapping, Any, Optional

BASE_AES_OID = "2.16.840.1.101.3.4.1"

AES_MODE_OID_MAP: dict[str, int] = {
    "ecb": 1,
    "cbc": 2,
    "ofb": 3,
    "cfb": 4,
    "kw": 5,
    "gcm": 6,
    "ccm": 7,
    "kwp": 8,
}

AES_KEYSIZE_OID_MAP: dict[int, int] = {
    192: 2,
    256: 4,
}


def aes_to_oid(comp: Mapping[str, Any], default_key_bits: int = 128) -> Optional[str]:

    name = str(comp.get("name", "")).strip().lower()
    if name != "aes":
        return None

    psi = comp.get("parameterSetIdentifier", "unknown")
    key_bits: Optional[int]
    try:
        key_bits = int(psi)
    except (TypeError, ValueError):
        key_bits = None

    if key_bits is None:
        key_bits = default_key_bits

    mode = comp.get("mode")
    mode = None if mode in (None, "", "none") else str(mode).strip().lower()

    if key_bits is None:
        return BASE_AES_OID

    keysize_oid_number = AES_KEYSIZE_OID_MAP.get(key_bits)

    oid = BASE_AES_OID
    if keysize_oid_number is not None:
        oid += f".{keysize_oid_number}"

    if mode is None:
        return oid

    mode_oid_number = AES_MODE_OID_MAP.get(mode)
    if mode_oid_number is None:
        return oid

    if keysize_oid_number is None:
        oid += "."

    oid += str(mode_oid_number)
    return oid
