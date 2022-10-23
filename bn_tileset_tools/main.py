#!/usr/bin/env python3

from pathlib import Path
from rich import print
import typer
from typer import Option as Opt

from bn_tileset_tools.transform import get_tileset_ids

app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})


@app.command(name="id")
def tileset_ids(
    path: Path,
    pretty: bool = Opt(False, "--pretty", help="Pretty print the output."),
) -> None:
    """
    List all tileset ids in a tile_config.json file.
    You can also pass a directory containing it.
    """

    if path.is_dir():
        path /= "tile_config.json"

    ids = get_tileset_ids(path)
    print(ids if pretty else "\n".join(ids))


@app.command()
def decompose(path: Path) -> None:
    """
    Decompose a tile_config.json file into its constituent parts.
    """

    # from tileset_tools.decompose_tileset import decompose_tileset

    # decompose_tileset(path)
    print("TODO")


@app.command()
def migrate(path: Path) -> None:
    """
    Migrate a `tile_info.json` file into `tileset.json`.
    """


if __name__ == "__main__":
    app()
