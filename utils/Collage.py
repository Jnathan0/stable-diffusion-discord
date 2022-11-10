import numpy
import io
import asyncio
from PIL import Image

def make_collage_sync(images: list, wrap: int, config) -> io.BytesIO:
    image_arrays = [numpy.array(Image.open(image)) for image in images]
    for image in images:
        image.seek(0)
    collage_horizontal_arrays = [numpy.hstack(
        image_arrays[i:i + wrap]) for i in range(0, len(image_arrays), wrap)]
    collage_array = numpy.vstack(collage_horizontal_arrays)
    collage_image = Image.fromarray(collage_array)
    collage = io.BytesIO()
    collage_image.save(collage, format=config['COLLAGE_FORMAT'])
    collage.seek(0)
    return collage


async def make_collage(images: list, wrap: int, config) -> io.BytesIO:
    images = await asyncio.get_running_loop().run_in_executor(None, make_collage_sync, images, wrap, config)
    return images