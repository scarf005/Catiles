"""
RETRO DAYS TILESET
#Name of the tileset
NAME: retrodays
#Viewing (Option) name of the tileset
VIEW: RetroDays
#JSON Path - Default of gfx/tile_config.json
JSON: tile_config.json
#Tileset Path - Default of gfx/tinytile.png
TILESET: tiles.png
"""
# Example of a tileset.txt file

from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar
from flupy import flu
import re




@dataclass
class TilesetTxt:
    """
    Provides metadata about a tileset.
    """

    NAME: str
    VIEW: str
    JSON: str
    TILESET: str

    COMMENT: ClassVar = re.compile(r"^([^#]*)")
    WHITESPACE: ClassVar = re.compile(r"^\s*$")

    @classmethod
    def from_text(cls, text: str):
        res: list[tuple[str, str]] = (
            flu(text.splitlines())
            .map(lambda l: cls.COMMENT.match(l).group(1))  # type: ignore
            .filter(lambda l: not cls.WHITESPACE.match(l))  # remove empty lines
            .map(lambda l: l.split(":"))
            .map(lambda l: tuple(v.strip() for v in l))
            .collect()
        )
        return cls(**dict(res))

    @classmethod
    def from_path(cls, path: Path):
        return cls.from_text(path.read_text())


if __name__ == "__main__":
    txt = TilesetTxt.from_text(__doc__)  # type: ignore
    print(txt)
