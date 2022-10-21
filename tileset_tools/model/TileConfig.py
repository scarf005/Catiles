from pathlib import Path
from typing import Literal
import msgspec
from msgspec import Struct

ID = str | list[str]


class TileBase(Struct, omit_defaults=True):
    ...


class TileInfo(TileBase):
    height: int
    width: int
    iso: bool = False
    pixelscale: int = 1


class AdditionalTile(TileBase):
    id: ID
    fg: int | list[int]


class Tile(TileBase):
    id: ID
    fg: int | None = None
    bg: int | None = None
    rotates: bool = False
    multitile: bool = False
    additional_tiles: list[AdditionalTile] | None = None


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


class TileConfigBase(Struct, rename={"tiles_new": "tiles-new"}):
    ...


class TileConfig(TileConfigBase):
    tile_info: tuple[TileInfo]
    tiles_new: list[SpriteSheet]


if __name__ == "__main__":
    res = msgspec.json.decode(  # type: ignore
        Path("ASCIITileset/tile_config.json").read_bytes(), type=TileConfig  # type: ignore
    )
    Path("tile_config.json").write_bytes(msgspec.json.encode(res))