from msgspec import Struct


class TileEntry(Struct):
    id: str
    fg: str
    bg: str
