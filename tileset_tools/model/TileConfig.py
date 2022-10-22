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

class SpriteSheetBase(Struct, omit_defaults=True):
    tiles: list[Tile]

class SpriteSheet(SpriteSheetBase):
    file: str
    ascii: list[Ascii] | None = None

    sprite_width: int = 16
    sprite_height: int = 16
    sprite_offset_x: int = 0
    sprite_offset_y: int = 0
    pixelscale: float = 1.0


rename = {"tilesheets": "tiles-new"}


class TileConfigBase(Struct, rename=rename):
    ...


class TileConfig(
    TileConfigBase, rename=rename | {"_TileConfig__tile_info": "tile_info"}
):
    __tile_info: tuple[TileInfo]
    tilesheets: list[SpriteSheet]

    @property
    def tile_info(self) -> TileInfo:
        return self.__tile_info[0]


if __name__ == "__main__":
    res = msgspec.json.decode(  # type: ignore
        Path("ASCIITileset/tile_config.json").read_bytes(), type=TileConfig  # type: ignore
    )
    print(res.tile_info)
    print(len(res.tilesheets[0].tiles))
    Path("tile_config.json").write_bytes(msgspec.json.encode(res))
