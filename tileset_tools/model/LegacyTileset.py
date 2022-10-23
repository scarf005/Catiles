from typing import TypedDict


class __LegacyTilesetDefault(TypedDict, total=False):
    pixelscale: int


class LegacyTilesetDefault(__LegacyTilesetDefault):
    width: int
    height: int


class LegacyFillerValue(TypedDict):
    source: str
    exclude: list[str]


if __name__ == "__main__":
    from rich import print

    foo: LegacyTilesetDefault = {"width": 10, "height": 10, "pixelscale": 1}
    foo.get("pixelscale")
    print(foo)
