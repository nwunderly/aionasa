import asyncio
from aionasa.mars_photos.api import MarsPhotos


async def main():
    async with MarsPhotos() as client:
        manifest = await client.manifest('curiosity')
        print(manifest.name)
        print(manifest.total_photos, "photos")
        date = manifest.photos[0]
        print(date.total_photos, date.cameras)

        photos = await client.photos('curiosity', sol=1000)
        print(photos[0])



asyncio.run(main())
