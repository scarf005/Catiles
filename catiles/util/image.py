from io import BytesIO
from typing import NamedTuple

from aiopathlib import AsyncPath
from PIL import Image


class Box(NamedTuple):
    left: int
    upper: int
    right: int
    lower: int


async def save_image(path: AsyncPath, img: Image.Image) -> None:
    """Save Pillow Image asynchronously."""
    with BytesIO() as buffer:
        img.save(buffer, format="PNG")
        await path.write_bytes(buffer.getbuffer())
