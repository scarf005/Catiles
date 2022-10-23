import msgspec
from tileset_tools.model.TileConfig import TileConfig


tileconfig_decoder = msgspec.json.Decoder(TileConfig)
