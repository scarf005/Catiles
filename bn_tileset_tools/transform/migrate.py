from enum import IntEnum, auto
from typing import Any
from aiopathlib import AsyncPath
from flupy import flu
from pathlib import Path
from rich import print
from rich.progress import track, Progress

import msgspec
from bn_tileset_tools.model import (
    Filler,
    Tileset,
    TilesetDefault,
    Tilesheet,
)
from bn_tileset_tools.model.TileConfig import TileConfig
from bn_tileset_tools.transform.split_fallback import get_merged_fallbacks
from bn_tileset_tools.util.image import save_image


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


def tileset_from_legacy(tile_info: Path, fallback_path: Path) -> Tileset:
    values = (
        flu(msgspec.json.decode(tile_info.read_bytes()))
        .group_by(group_objects, sort=False)
        .collect()
    )

    kwargs: dict[str, Any] = {"fallback": str(fallback_path)}
    for value in track(values, description="Converting to tileset"):
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

    return Tileset(**kwargs)


if __name__ == "__main__":
    root = Path("example/ascii")
    info = root / "tile_info.json"
    config = root / "tile_config.json"

    tileset_from_legacy(info, config)
