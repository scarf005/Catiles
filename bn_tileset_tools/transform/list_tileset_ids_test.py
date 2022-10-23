from bn_tileset_tools.transform import get_tileset_ids
from bn_tileset_tools.examples import ascii_path


def test_get_tileset_ids():
    ids = get_tileset_ids(ascii_path / "tile_config.json")
    assert len(ids) == 56
