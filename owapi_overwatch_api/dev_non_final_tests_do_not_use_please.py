import asyncio
from owapi_overwatch_api import overwatch_api_async as owapi

"""DO NOT USE THIS AS A REAL TEST OF ANY KIND
THIS IS USED BY @drummersbrother TO TEST THE API SINCE IT'S NOT DONE
@drummersbrother committed this to so one can see how to use the api.
"""

async def testing(loop):
    client = owapi.async_owapi_api()
    print((await client.get_full_profile("Danielfrogs#2552"))["eu"])

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(testing(loop))