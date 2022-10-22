from pathlib import Path
from tileset_tools.list_tileset_ids import get_tileset_ids


def test_get_tileset_ids():
    ids = get_tileset_ids(Path("ASCIITileset/tile_config.json"))
    assert len(ids) == 56
