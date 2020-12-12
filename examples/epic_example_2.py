import os
import asyncio

from aionasa import EPIC


"""
A sample script that downloads all enhanced images from the most recent date
to a new folder called 'epic-images' in the current working directory.
"""


# define an async function to run the script in
async def main():

    # set up the client
    async with EPIC(api_key="DEMO_KEY") as epic:

        # get the image data from the API
        # this method defaults to the most recent date with available images
        images = await epic.enhanced_images()

        # the images will be downloaded to a new folder
        os.mkdir('epic-images')
        os.chdir('epic-images')

        # the library allows for images to be downloaded easily with the
        # asynchronous Asset.save() method.
        n = 0
        for image in images:
            await image.save()
            n += 1

        print(f'Downloaded {n} images.')


# run the 'main' coroutine
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
