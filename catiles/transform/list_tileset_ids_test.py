from catiles.transform import get_tileset_ids
from catiles.examples import ASCII_PATH


def test_get_tileset_ids():
    ids = get_tileset_ids(ASCII_PATH / "tile_config.json")
    assert len(ids) == 56
