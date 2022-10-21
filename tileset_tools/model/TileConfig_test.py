from tileset_tools.model.TileConfig import TileConfig
from tileset_tools.util.json_utils import json_bytes

from msgspec.json import decode, encode  # type: ignore


# def test_decode():
#     TEXT = json_bytes(
#         {
#             "tile_info": [
#                 {"height": 32, "width": 32, "iso": True, "pixelscale": 2}
#             ]
#             "tiles-new": [data=]
#         }
#     )
#     decoded = decode(TEXT, type=TileConfig)

#     print(decoded)
#     assert 0


TILE_CONFIG = {  # whole file is a single object
    "tile_info": [  # tile_info is mandatory
        {
            "height": 32,
            "width": 32,
            "iso": True,  #  Optional. Indicates an isometric tileset. Defaults to False.
            "pixelscale": 2,  #  Optional. Sets a multiplier for resizing a tileset. Defaults to 1.
        }
    ],
    "tiles-new": [  # tiles-new is an array of sprite sheets
        {  #   alternately, just one "tiles" array
            "file": "tiles.png",  # file containing sprites in a grid
            "tiles": [  # array with one entry per tile
                {
                    "id": "10mm",  # id is how the game maps things to sprites
                    "fg": 1,  #   lack of prefix mostly indicates items
                    "bg": 632,  # fg and bg can be sprite indexes in the image
                    "rotates": False,
                },
                {
                    "id": "t_wall",  # "t_" indicates terrain
                    "fg": [
                        2918,
                        2919,
                        2918,
                        2919,
                    ],  # 2 or 4 sprite numbers indicates pre-rotated
                    "bg": 633,
                    "rotates": True,
                    "multitile": True,
                    "additional_tiles": [  # connected/combined versions of sprite
                        {  #   or variations, see below
                            "id": "center",
                            "fg": [2919, 2918, 2919, 2918],
                        },
                        {"id": "corner", "fg": [2924, 2922, 2922, 2923]},
                        {"id": "end_piece", "fg": [2918, 2919, 2918, 2919]},
                        {"id": "t_connection", "fg": [2919, 2918, 2919, 2918]},
                        {"id": "unconnected", "fg": 2235},
                    ],
                },
                {
                    "id": "vp_atomic_lamp",  # "vp_" vehicle part
                    "fg": 3019,
                    "bg": 632,
                    "rotates": False,
                    "multitile": True,
                    "additional_tiles": [
                        {"id": "broken", "fg": 3021}  # variant sprite
                    ],
                },
                {
                    "id": "t_dirt",
                    "rotates": False,
                    "fg": [
                        {
                            "weight": 50,
                            "sprite": 640,
                        },  # weighted random variants
                        {"weight": 1, "sprite": 3620},
                        {"weight": 1, "sprite": 3621},
                        {"weight": 1, "sprite": 3622},
                    ],
                },
                {
                    "id": [
                        "overlay_mutation_GOURMAND",  # character overlay for mutation
                        "overlay_mutation_male_GOURMAND",  # overlay for specified gender
                        "overlay_mutation_active_GOURMAND",  # overlay for activated mutation
                    ],
                    "fg": 4040,
                },
            ],
        },
        {  # second entry in tiles-new
            "file": "moretiles.png",  # another sprite sheet
            "tiles": [
                {
                    "id": ["xxx", "yyy"],  # define two ids at once
                    "fg": 1,
                    "bg": 234,
                }
            ],
        },
    ],
    "overlay_ordering": [
        {
            "id": "WINGS_BAT",  # mutation name, in a string or array of strings
            "order": 1000,  # range from 0 - 9999, 9999 being the topmost layer
        },
        {
            "id": [
                "PLANTSKIN",
                "BARK",
            ],  # mutation name, in a string or array of strings
            "order": 3500,  # order is applied to all items in the array
        },
        {
            "id": "bio_armor_torso",  # Overlay order of bionics is controlled in the same way
            "order": 500,
        },
    ],
}
