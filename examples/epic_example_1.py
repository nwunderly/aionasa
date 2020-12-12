import asyncio
import random

from aionasa import EPIC


"""
A sample script that prints out data on a random EPIC image.
"""


# define an async function to run the script in
async def main():

    # set up the client
    async with EPIC(api_key="DEMO_KEY") as epic:

        # get list of dates with available natural color images
        dates = await epic.natural_listing()

        # we're going to pick a random date to request the data for
        date = random.choice(dates)
        print(f'getting images available for {date}.')

        # get the images for that date
        images = await epic.natural_images(date)
        print(f'found {len(images)} images.')

        # pick a random image
        image = random.choice(images)

        # print some information about that image
        print(f"Image filename: {image.filename}\n"
              f"Image url: {image.png_url}\n"
              f"Caption: {image.caption}\n")


# run the 'main' coroutine
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
