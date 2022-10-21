import json
from msgspec import Struct


class TileMeta(Struct):
    width: int
    height: int
    pixelscale: int = 1


