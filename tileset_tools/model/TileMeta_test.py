from tileset_tools.model.TileMeta import TileMeta
from tileset_tools.util.test_utils import json_bytes

from msgspec.json import decode, encode  # type: ignore


def test_full():
    expected = TileMeta(32, 32, 1)
    b = json_bytes({"width": 32, "height": 32, "pixelscale": 1})

    decoded = decode(b, type=TileMeta)
    assert decoded == expected

    encoded = encode(decoded)
    assert encoded == b


def test_partial():
    expected = TileMeta(32, 32, 1)
    b = json_bytes({"width": 32, "height": 32})

    decoded = decode(b, type=TileMeta)
    assert decoded == expected
