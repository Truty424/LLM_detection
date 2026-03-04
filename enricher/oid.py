from typing import Optional

from .aes import aes_to_oid
# To do: in future
# from .xxx import xxx_to_oid



def to_oid(component: dict) -> Optional[str]:
    """
    Dispatch OID resolution to the correct algorithm-specific enricher.
    """

    name = str(component.get("name", "")).lower()

    if name == "aes":
        return aes_to_oid(component)

    # To do: in future
    # if name == "xxx":
    #     return xxx_to_oid(component) ...

    return None
