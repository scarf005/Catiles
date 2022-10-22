from flupy import flu
import msgspec
from pathlib import Path

from tileset_tools.model.TileConfig import TileConfig
from tileset_tools.util import lift_list

id_decoder = msgspec.json.Decoder(TileConfig)


def get_tileset_ids(config: TileConfig | Path) -> list[str]:
    match config:
        case Path():
            tilesheets = id_decoder.decode(config.read_bytes()).tilesheets
        case _:
            tilesheets = config.tilesheets

    return (
        flu(tilesheets)
        .map(lambda x: x.tiles)
        .map(lambda x: flu(x).map(lambda y: lift_list(y.id)))
        .flatten(depth=2)
        .to_list()
    )
