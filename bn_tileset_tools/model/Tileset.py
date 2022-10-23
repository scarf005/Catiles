from msgspec import Struct

from bn_tileset_tools.model.LegacyTileset import (
    LegacyFiller,
    LegacyTilesetDefault,
    LegacyTilesheet,
    LegacyTilesheetValue,
)


class TilesetBase(Struct, omit_defaults=True, frozen=True):
    ...


class Dimension(TilesetBase, omit_defaults=True):
    scale: int = 1
    col: int = 16
    x: int = 0
    y: int = 0

    @classmethod
    def from_legacy_tilesheet(cls, legacy: LegacyTilesheetValue):
        kwargs: dict[str, int] = {}

        if "sprite_width" in legacy:
            kwargs["x"] = legacy["sprite_width"]
        if "sprite_height" in legacy:
            kwargs["y"] = legacy["sprite_height"]
        if "pixelscale" in legacy:
            kwargs["scale"] = legacy["pixelscale"]
        if "sprites_accross" in legacy:
            kwargs["col"] = legacy["sprites_accross"]

        return cls(**kwargs)

    @classmethod
    def from_legacy_default(cls, legacy: LegacyTilesetDefault):
        if "pixelscale" in legacy:
            return cls(scale=legacy["pixelscale"])
        else:
            return cls()


class Sprite(Struct):
    """Sprite width and height.

    :param width: Width of the sprite.
    :param height: Height of the sprite.
    """

    w: int = 32
    h: int = 32

    @classmethod
    def from_legacy(cls, legacy: LegacyTilesetDefault | LegacyTilesheetValue):
        match legacy:
            case {"width": w, "height": h}:
                return cls(w=w, h=h)
            case {"sprite_width": w, "sprite_height": h}:
                return cls(w=w, h=h)
            case _:
                return cls()


class TilesetDefault(TilesetBase):
    """Default values applied to all sheets and fallbacks."""

    sprite: Sprite
    dimentsion: Dimension | None = None

    @classmethod
    def from_legacy(cls, legacy: LegacyTilesetDefault):
        sprite = Sprite(w=legacy["width"], h=legacy["height"])
        dimension = Dimension.from_legacy_default(legacy)
        return cls(sprite, dimension)


class Tilesheet(TilesetBase):
    file: str
    dimension: Dimension | None = None
    sprite: Sprite | None = None

    @classmethod
    def from_legacy(cls, legacy: LegacyTilesheet):
        file, value = next(iter(legacy.items()))
        dimension = Dimension.from_legacy_tilesheet(value)
        return cls(file, dimension)


class Filler(TilesetBase):
    source: str
    exclude: list[str]

    @classmethod
    def from_legacy(cls, legacy: LegacyFiller):
        source, value = next(iter(legacy.items()))
        return cls(source, value["exclude"])


class Tileset(TilesetBase):
    """
    New compositing tileset format
    """

    default: TilesetDefault
    sheet: list[Tilesheet]
    fallback: str
    filler: Filler | None = None
