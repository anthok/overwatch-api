import asyncio

import aiohttp

from overwatch_api.core import AsyncOWAPI
from overwatch_api.constants import *

"""DO NOT USE THIS AS A REAL TEST OF ANY KIND
THIS IS USED BY @drummersbrother TO TEST THE API SINCE IT'S NOT DONE
@drummersbrother committed this to so one can see how to use the api.
"""


async def testing(loop):
    # Instantiating the api
    client = AsyncOWAPI()

    data = {}

    # We use our own clientsession to demonstrate that it's possible to pool connections in that way
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        # We await an api method and get a dict back as a result
        # We pass our session, and we pass the platform we want results for, in this case it's PC and we don't actually need to pass, since it's a default
        print('Testing......[get_profile]')
        data[PC] = await client.get_profile("Danielfrogs#2552", session=session, platform=PC)
        print('Testing......[get_profile]')
        data[XBOX] = await client.get_profile("Danielfrogs#2552", session=session, platform=XBOX)
        print('Testing......[get_profile]')
        data[PLAYSTATION] = await client.get_profile("Danielfrogs#2552", session=session, platform=PLAYSTATION)
        print('Testing......[get_stats]')
        data[PC] = await client.get_stats("Danielfrogs#2552", session=session, platform=PC)
        print('Testing......[get_stats]')
        data[XBOX] = await client.get_stats("Danielfrogs#2552", session=session, platform=XBOX)
        print('Testing......[get_stats]')
        data[PC] = await client.get_stats("Danielfrogs#2552", session=session, platform=PLAYSTATION)
        print('Testing......[get_achievements]')
        data[PC] = await client.get_achievements("Danielfrogs#2552", session=session, platform=PC)
        print('Testing......[get_hero_stats]')
        data[PC] = await client.get_hero_stats("Danielfrogs#2552", session=session, platform=PC)

    print(data)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(testing(loop))