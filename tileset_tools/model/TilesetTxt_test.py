from tileset_tools.model.TilesetTxt import TilesetTxt


TEXT = """
    #RETRO DAYS TILESET
    #Name of the tileset
    NAME: retrodays # Foo


    #Viewing (Option) name of the tileset
    VIEW: RetroDays
    #JSON Path - Default of gfx/tile_config.json
    JSON: tile_config.json
    #Tileset Path - Default of gfx/tinytile.png
    TILESET: tiles.png
    """


def test_TilesetTxt():
    expected = TilesetTxt(
        "retrodays", "RetroDays", "tile_config.json", "tiles.png"
    )
    assert TilesetTxt.from_text(TEXT) == expected
