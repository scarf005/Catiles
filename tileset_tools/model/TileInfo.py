from msgspec import Struct


class TileMeta(Struct, frozen=True):
    """
    TileMeta is a struct that contains metadata about a tileset.
    """

    width: int
    height: int
    pixelscale: int = 1


TileInfo = tuple[TileMeta, ]

"""
[
  {
    "height": 10,
    "width": 10
  },
  {
    "ASCIITiles.png": { "//": "indices 0 to 79" }
  },
  {
    "fallback.png": { "fallback": true }
  }
]
"""
