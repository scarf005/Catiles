from typing import TypedDict


class __LegacyTilesetDefault(TypedDict, total=False):
    pixelscale: int


class LegacyTilesetDefault(__LegacyTilesetDefault):
    width: int
    height: int


class LegacyFillerValue(TypedDict):
    source: str
    exclude: list[str]


LegacyFiller = dict[str, LegacyFillerValue]


class __LegacyTileSheetSprite(TypedDict):
    sprite_width: int
    sprite_height: int


class __LegacyTileSheetOffset(TypedDict):
    sprite_offset_x: int
    sprite_offset_y: int


class LegacyTilesheetValue(
    __LegacyTileSheetSprite,
    __LegacyTileSheetOffset,
    total=False,
):
    pixelscale: int
    sprites_accross: int


LegacyTilesheet = dict[str, LegacyTilesheetValue]


if __name__ == "__main__":
    from rich import print

    foo: LegacyTilesetDefault = {"width": 10, "height": 10, "pixelscale": 1}
    foo.get("pixelscale")
    print(foo)
