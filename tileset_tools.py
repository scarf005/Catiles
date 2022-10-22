#!/usr/bin/env python3

from pathlib import Path
from pprint import pprint
import typer

from tileset_tools.list_tileset_ids import get_tileset_ids

app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})


@app.command(name="id")
def tileset_ids(path: Path):
    """
    List all tileset ids in a tile_config.json file.
    """

    if path.is_dir():
        path /= "tile_config.json"

    pprint(get_tileset_ids(path))


@app.command()
def decompose(path: Path):
    """
    Decompose a tile_config.json file into its constituent parts.
    """

    # from tileset_tools.decompose_tileset import decompose_tileset

    # decompose_tileset(path)
    print("TODO")


if __name__ == "__main__":
    app()
