import json
from pprint import pprint
from re import S
from typing import Any, Literal
import msgspec
from msgspec import Struct


class TileInfo(Struct, omit_defaults=True):
    height: int
    width: int
    iso: bool = False
    pixelscale: int = 1


class Tile(Struct, omit_defaults=True):
    id: str | list[str]
    fg: int | None = None
    bg: int | None = None
    rotates: bool = False


class Ascii(Struct):
    offset: int
    bold: bool
    color: Literal[
        "WHITE", "BLACK", "RED", "YELLOW", "GREEN", "CYAN", "BLUE", "MAGENTA"
    ]


class SpriteSheet(Struct, omit_defaults=True):
    file: str
    tiles: list[Tile]
    ascii: list[Ascii] | None = None


class TileConfig(Struct, rename={"tiles_new": "tiles-new"}):
    tile_info: tuple[TileInfo]
    tiles_new: list[SpriteSheet]


if __name__ == "__main__":
    from pathlib import Path

    res = msgspec.json.decode(  # type: ignore
        Path("ASCIITileset/tile_config.json").read_bytes(), type=TileConfig
    )
    # pprint(res)
    Path("tile_config.json").write_bytes(msgspec.json.encode(res))
