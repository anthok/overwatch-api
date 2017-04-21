import asyncio

import aiohttp

from owapi_overwatch_api import overwatch_api_async as owapi
from owapi_overwatch_api.constants import *

"""DO NOT USE THIS AS A REAL TEST OF ANY KIND
THIS IS USED BY @drummersbrother TO TEST THE API SINCE IT'S NOT DONE
@drummersbrother committed this to so one can see how to use the api.
"""

async def testing(loop):
    # Instantiating the api
    client = owapi.async_owapi_api()

    blob = {}
    stats = {}

    # We use our own clientsession to demonstrate that it's possible to pool connections in that way
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        # We await an api method and get a dict back as a result
        # We pass our session, and we pass the platform we want results for, in this case it's PC and we don't actually need to pass, since it's a default
        blob[PC] = await client.get_profile("Danielfrogs#2552", session=session, platform=PC)
        print("lmao")
        # We sleep to avoid getting a owapi_overwatch_api.exceptions.RatelimitError (http 429 code from the api)
        await asyncio.sleep(5)
        blob[XBOX] = await client.get_profile("Danielfrogs#2552", session=session, platform=XBOX)
        print("lmao")
        await asyncio.sleep(5)
        blob[PLAYSTATION] = await client.get_profile("Danielfrogs#2552", session=session, platform=PLAYSTATION)
        print("I'm done now")
        await asyncio.sleep(5)
        stats[PC] = await client.get_stats("Danielfrogs#2552", session=session, platform=PC)
        print("lmao")
        await asyncio.sleep(5)
        stats[XBOX] = await client.get_stats("Danielfrogs#2552", session=session, platform=XBOX)
        print("lmao")
        await asyncio.sleep(5)
        stats[PLAYSTATION] = await client.get_stats("Danielfrogs#2552", session=session, platform=PLAYSTATION)
        print("done yet again")
    print(blob)
    print(stats)
    print(blob[PC][EUROPE]["stats"] == stats[PC][EUROPE])

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(testing(loop))