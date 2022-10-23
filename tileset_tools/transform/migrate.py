from enum import IntEnum, auto
from typing import Any
from flupy import flu
from pathlib import Path
from rich import print
from rich.progress import track

import msgspec
from tileset_tools.transform import tileconfig_decoder
from tileset_tools.model import (
    Filler,
    Tileset,
    TilesetDefault,
    Tilesheet,
)


class LegacyType(IntEnum):
    DEFAULT = auto()
    TILESHEET = auto()
    FALLBACK = auto()
    FILLER = auto()


LegacyObject = dict[str, Any]


def group_objects(obj: LegacyObject) -> LegacyType:
    def match_inner(obj: LegacyObject) -> LegacyType:
        match obj:
            case {"filler": True}:
                return LegacyType.FILLER
            case {"fallback": True}:
                return LegacyType.FALLBACK
            case _:
                return LegacyType.TILESHEET

    match obj:
        case {"width": _, "height": _}:
            return LegacyType.DEFAULT
        case _:
            return match_inner(next(iter(obj.values())))


def migrate_from(tile_info: Path, tile_config: Path) -> Tileset:
    values = (
        flu(msgspec.json.decode(tile_info.read_bytes()))
        .group_by(group_objects, sort=False)
        .collect()
    )

    kwargs: dict[str, Any] = {"fallback": Path("fallback")}
    for value in track(values, description="Converting"):
        match value:
            case (LegacyType.DEFAULT, default):
                kwargs["default"] = TilesetDefault.from_legacy(default.first())
            case (LegacyType.TILESHEET, sheets):
                kwargs["sheet"] = (
                    flu(sheets).map(Tilesheet.from_legacy).to_list()
                )
            case (LegacyType.FILLER, filler):
                kwargs["filler"] = Filler.from_legacy(filler.first())
            case _:
                pass

    tileset = Tileset(**kwargs)
    print(tileset)

    res = tileconfig_decoder.decode(tile_config.read_bytes())
    print(res.fallback.ascii)
    return tileset


if __name__ == "__main__":
    root = Path("example/ascii")
    info = root / "tile_info.json"
    config = root / "tile_config.json"

    migrate_from(info, config)
