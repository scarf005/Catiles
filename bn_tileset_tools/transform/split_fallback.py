from typing import Final
from flupy import flu
from flupy.fluent import Fluent
from pathlib import Path
from rich.progress import track
from PIL import Image

from bn_tileset_tools.model.TileConfig import Ascii, AsciiColor, TileConfig
from bn_tileset_tools.util.image import Box


def split_fallback(path: Path) -> list[Image.Image]:
    image = Image.open(path)
    NUM_COLORS: Final[int] = 16

    w, h = image.size
    color_height = h // NUM_COLORS

    heights = track(
        range(0, h, color_height), description="Splitting fallbacks"
    )
    return [image.crop(Box(0, y, w, y + color_height)) for y in heights]


def merge_vertically(up: Image.Image, down: Image.Image) -> Image.Image:
    dest = Image.new("RGBA", (up.width, up.height + down.height))
    dest.paste(up, (0, 0))
    dest.paste(down, (0, up.height))
    return dest


AsciiPair = tuple[Ascii, Image.Image]
AsciiArgs = tuple[AsciiColor, Fluent[AsciiPair]]


def __is_bold(pair: AsciiPair) -> bool:
    ascii, _ = pair
    return not ascii.bold


def __by_bold(args: AsciiArgs):
    color, pairs = args
    return color, pairs.sort(__is_bold).collect()


def __get_merged_fallback(args: AsciiArgs):
    color, pairs = args
    return color, merge_vertically(*flu(pairs).map(lambda x: x[1]).collect())


def get_merged_fallbacks(path: Path, config: TileConfig):
    """get list of splitted fallbacks, each merged vertically by boldness"""
    images = split_fallback(path / config.fallback.file)
    asciis = config.fallback.ascii
    assert asciis
    return (
        flu(zip(asciis, images))
        .group_by(lambda pair: pair[0].color)
        .map(__by_bold)  # type: ignore
        .map(__get_merged_fallback)  # type: ignore
        .collect()
    )
