import json
from typing import Any


def json_bytes(data: dict[str, Any]):
    return bytes(
        json.dumps(
            data,
            separators=(",", ":"),
        ),
        encoding="utf-8",
    )
