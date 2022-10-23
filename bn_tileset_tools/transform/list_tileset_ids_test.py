from bn_tileset_tools.transform import get_tileset_ids
from bn_tileset_tools.examples import ASCII_PATH


def test_get_tileset_ids():
    ids = get_tileset_ids(ASCII_PATH / "tile_config.json")
    assert len(ids) == 56
