#!/usr/bin/env python3

from pathlib import Path
from aiopathlib import AsyncPath
import msgspec
from rich import print
from rich.progress import track
import typer
from typer import Option as Opt
from rich.console import Console
from asyncio import run as aiorun
from catiles.model.TileConfig import TileConfig
from catiles.util import coro, save_image

app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})
console: Console = Console()


@app.command(name="id")
def tileset_ids(
    path: Path,
    pretty: bool = Opt(False, "--pretty", help="Pretty print the output."),
) -> None:
    """
    List all tileset ids in a tile_config.json file.
    You can also pass a directory containing it.
    """
    from catiles.transform import get_tileset_ids

    if path.is_dir():
        path /= "tile_config.json"

    ids = get_tileset_ids(path)
    print(ids if pretty else "\n".join(ids))


@app.command()
async def decompose(path: Path) -> None:
    """
    Decompose a tile_config.json file into its constituent parts.
    """

    # from tileset_tools.decompose_tileset import decompose_tileset

    # decompose_tileset(path)
    print("TODO")


@app.command()
@coro
async def migrate(path: Path) -> None:
    """
    Migrate into bntools compatible tileset.json.

    given directory should contain a tile_config.json and a tile_info.json
    """
    import json
    from catiles.transform import (
        tileset_from_legacy,
        get_merged_fallbacks,
    )

    tile_info = path / "tile_info.json"
    tile_config = path / "tile_config.json"
    fallback = AsyncPath(path) / "fallback"
    tileset_path = AsyncPath(path) / "tileset.json"

    config = msgspec.json.decode(tile_config.read_bytes(), type=TileConfig)
    tileset = tileset_from_legacy(tile_info, fallback)

    encoded = msgspec.json.encode(tileset)
    await tileset_path.write_text(json.dumps(json.loads(encoded), indent=2))

    await fallback.mkdir(parents=True, exist_ok=True)
    fallbacks = get_merged_fallbacks(path, config)
    for name, img in track(fallbacks, description="Saving fallbacks"):
        await save_image(fallback / f"{name}.png", img)


if __name__ == "__main__":
    aiorun(app())
