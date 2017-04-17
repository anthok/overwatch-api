import aiohttp
import async_timeout
from .constants import *

"""The async interface to the OWAPI (https://github.com/SunDwarf/OWAPI) api."""

class async_owapi_api(object):
    """The async client object to use when you want to use the OWAPI api.
    All requests throw ConnectionError if they can't connect or similar problem.
    Other exceptions should be reported as bugs if they're raised."""

    def __init__(self, default_platform: str=PC, server_url: str="https://owapi.net"):
        """Creates and sets up the client object."""

        # Stuff the user should have control over
        self.server_url = server_url
        self.default_platform = default_platform

        # If you're and advanced user you maybe, sometime, idk, probably, might want to control these
        self._api_version = 3
        self._api_urlpath = "/api/v{0}/u/".format(self._api_version)

    def _uses_aiohttp_session(func):
        """This is a decorator that creates an async with statement around a function, and makes sure that a _session argument is always passed.
        Only usable on async functions of course.
        The _session argument is (supposed to be) an aiohttp.ClientSession instance in all functions that this decorator has been used on.
        This is used to make sure that all session objects are properly entered and exited, or that they are passed into a function properly.
        This adds an session keyword argument to the method signature, and that session will be used as _session if it is not None."""

        # The function the decorator returns
        async def decorated_func(*args, session=None, **kwargs):
            if session is not None:
                # There is a session passed
                session.connector = aiohttp.TCPConnector(verify_ssl=False)
                return await func(*args, _session=session, **kwargs)
            else:
                # The session argument wasn't passed, so we create our own
                async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as new_session:
                    return await func(*args, _session=new_session, **kwargs)

        # We return the decorated func
        return decorated_func

    @_uses_aiohttp_session
    async def get_full_profile(self, battletag: str, _session=None):
        return await self._base_request(battletag, "blob", _session)

    @staticmethod
    def validate_response(response):
        """Used to check that the response from the api was correct/proper."""
        if response.status != 200:
            raise ConnectionError

    @staticmethod
    def sanitize_battletag(battle_tag: str) -> str:
        """In the api, battletags' #:s are replaced with dashes, this method does that."""
        if "#" in battle_tag:
            battle_tag = battle_tag.replace("#", "-")
        return battle_tag

    async def _base_request(self, battle_tag: str, endpoint_name: str, session: aiohttp.ClientSession, platform=None):
        """Does a request to some endpoint."""
        if platform is None:
            platform = self.default_platform

        san_battle_tag = self.sanitize_battletag(battle_tag)
        resp_json, status = await self._async_get(
            session,
            self.server_url + self._api_urlpath + "{battle_tag}/{endpoint}".format(
                battle_tag=san_battle_tag,
                endpoint=endpoint_name
            ),
            params={"platform": platform}, # Passed to _async_get and indicates what platform we're searching on
            headers={"User-Agent": "overwatch_python_api"} # According to https://github.com/SunDwarf/OWAPI/blob/master/owapi/v3/v3_util.py#L18 we have to customise our User-Agent, so we do
        )

        # Validate the response
        if status != 200:
            raise ConnectionError
        return resp_json


    async def _async_get(self, session: aiohttp.ClientSession, *args, _async_timeout_seconds: int=5,  **kwargs) -> aiohttp.ClientResponse:
        """Uses aiohttp to make a get request instead of using requests. 
        Will raise asyncio.TimeoutError if the request could not be completed 
        within _async_timeout_seconds (default 5) seconds."""

        # Taken almost directly from the aiohttp tutorial
        with async_timeout.timeout(_async_timeout_seconds):
            async with session.get(*args, **kwargs) as response:
                return await response.json(), response.status
