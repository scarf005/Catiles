from flupy import flu
from pathlib import Path

import msgspec

from bn_tileset_tools.model.TileConfig import TileConfig
from bn_tileset_tools.util import lift_list


def get_tileset_ids(config: TileConfig | Path) -> list[str]:
    match config:
        case Path():
            tilesheets = msgspec.json.decode(config.read_bytes()).tilesheets
        case _:
            tilesheets = config.tilesheets

    return (
        flu(tilesheets)
        .map(lambda x: x.tiles)
        .map(lambda x: flu(x).map(lambda y: lift_list(y.id)))
        .flatten(depth=2)
        .to_list()
    )
