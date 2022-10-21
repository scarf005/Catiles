from flupy import flu
from msgspec import Struct
import msgspec
from pathlib import Path

from tileset_tools.model.TileConfig import TileConfigBase
from tileset_tools.util import lift_list


class TileID(Struct):
    id: str | list[str]


class TileIDSheet(Struct):
    tiles: list[TileID]


class TileIDs(TileConfigBase):
    tiles_new: list[TileIDSheet]


id_decoder = msgspec.json.Decoder(TileIDs)


def get_tileset_ids(path: Path) -> list[str]:
    tiles_new = id_decoder.decode(path.read_bytes()).tiles_new
    res: list[str] = (
        flu(tiles_new)
        .map(lambda x: x.tiles)
        .map(lambda x: flu(x).map(lambda y: lift_list(y.id)))
        .flatten(depth=2)
        .collect()  # type: ignore
    )
    return res
