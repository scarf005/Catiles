import msgspec
from bn_tileset_tools.model import TileConfig


tileconfig_decoder = msgspec.json.Decoder(TileConfig)
