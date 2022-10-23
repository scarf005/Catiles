from enum import IntEnum, auto
from typing import Any
from flupy import flu
from pathlib import Path
import json
from rich import print
from tileset_tools.model.LegacyTileset import (
    LegacyFiller,
    LegacyTilesetDefault,
    LegacyTilesheet,
)

from tileset_tools.model.Tileset import Filler, TilesetDefault, Tilesheet


class LegacyType(IntEnum):
    DEFAULT = auto()
    TILESHEET = auto()
    FALLBACK = auto()
    FILLER = auto()


def group_objects(obj: dict[str, Any]) -> LegacyType:
    def match_inner(obj: dict[str, Any]) -> LegacyType:
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


text = Path("example/tile_info/example.json").read_text()

values = (
    flu(json.loads(text))
    .group_by(group_objects, sort=False)
    .map(lambda x: x[1])
    .collect()
)
if len(values) == 4:
    default, sheet, filler, _ = values
    print(Filler.from_legacy(filler.first()))
else:
    default, sheet, _ = values

print(
    TilesetDefault.from_legacy(default.first()),
    sheet.map(Tilesheet.from_legacy).collect(),
)
