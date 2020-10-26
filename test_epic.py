import asyncio
import datetime

from aionasa.epic import EPIC
from API_KEY import API_KEY


async def main():

    async with EPIC(api_key=API_KEY) as epic:

        data = await epic.natural()

    yyyy, mm, dd = data[0]['date'].split()[0].split('-')

    print(f"https://api.nasa.gov/EPIC/archive/natural/{yyyy}/{mm}/{dd}/png/{data[0]['image']}.png?api_key={API_KEY}")
    print(len(data))



if __name__ == '__main__':
    asyncio.run(main())


##################################################################################################
#                               SAMPLE RESPONSE BELOW
##################################################################################################
_ = {
    'identifier': '20201024004554',
    'caption': "This image was taken by NASA's EPIC camera onboard the NOAA DSCOVR spacecraft",
    'image': 'epic_1b_20201024004554',
    'version': '03',
    'centroid_coordinates': {'lat': -9.23584, 'lon': 176.652832},
    'dscovr_j2000_position': {'x': -1108155.716667, 'y': -951452.105977, 'z': -236890.272495},
    'lunar_j2000_position': {'x': 230140.370362, 'y': -276401.001087, 'z': -146834.754073},
    'sun_j2000_position': {'x': -127828985.600038, 'y': -69876339.964046, 'z': -30291110.799975},
    'attitude_quaternions': {'q0': 0.60256, 'q1': 0.15611, 'q2': 0.31807, 'q3': 0.71511},
    'date': '2020-10-24 00:41:06',
    'coords': {
        'centroid_coordinates': {'lat': -9.23584, 'lon': 176.652832},
        'dscovr_j2000_position': {'x': -1108155.716667, 'y': -951452.105977, 'z': -236890.272495},
        'lunar_j2000_position': {'x': 230140.370362, 'y': -276401.001087, 'z': -146834.754073},
        'sun_j2000_position': {'x': -127828985.600038, 'y': -69876339.964046, 'z': -30291110.799975},
        'attitude_quaternions': {'q0': 0.60256, 'q1': 0.15611, 'q2': 0.31807, 'q3': 0.71511}
        }
    }

