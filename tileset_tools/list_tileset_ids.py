from flupy import flu
from msgspec import Struct
import msgspec
from pathlib import Path


from tileset_tools.model.TileConfig import ID, TileConfig, TileConfigBase
from tileset_tools.util import lift_list


class TileID(Struct):
    id: ID


class TileIDSheet(Struct):
    tiles: list[TileID]


class TileIDs(TileConfigBase):
    tiles_new: list[TileIDSheet]


id_decoder = msgspec.json.Decoder(TileIDs)


def get_tileset_ids(config: TileIDs | TileConfig | Path) -> list[str]:
    match config:
        case Path():
            tiles_new = id_decoder.decode(config.read_bytes()).tiles_new
        case _:
            tiles_new = config.tiles_new

    return (
        flu(tiles_new)
        .map(lambda x: x.tiles)
        .map(lambda x: flu(x).map(lambda y: lift_list(y.id)))
        .flatten(depth=2)
        .to_list()
    )
