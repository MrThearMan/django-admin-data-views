import re

__all__ = [
    "exact",
]


def exact(msg: str) -> str:
    """Use in `with pytest.raises(..., match=exact(msg))` to match the 'msg' string exactly."""
    return f"^{re.escape(msg)}$"
