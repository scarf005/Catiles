from msgspec import Struct


class TileMeta(Struct, frozen=True):
    """
    TileMeta is a struct that contains metadata about a tileset.
    """

    width: int
    height: int
    pixelscale: int = 1


class SheetMeta(Struct, frozen=True, omit_defaults=True):
    fallback: bool = False



TEXT = b"""
[
  { "height": 10, "width": 10 },
  { "ASCIITiles.png": { "//": "indices 0 to 79" } },
  { "fallback.png": { "fallback": true } }
]
"""

if __name__ == "__main__":
    from msgspec import json

    decoder = json.Decoder(list[TileMeta])
    print(decoder.decode(TEXT))
