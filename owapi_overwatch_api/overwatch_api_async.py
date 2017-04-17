import aiohttp
import async_timeout

from .constants import *
from .exceptions import *

"""The async interface to the OWAPI (https://github.com/SunDwarf/OWAPI) api."""


# TODO Handle being ratelimited, asyncio.sleep?

class async_owapi_api(object):
    """The async client object to use when you want to use the OWAPI api.
    All requests throw ConnectionError if they can't connect or similar problem.
    Other exceptions should be reported as bugs if they're raised."""

    def __init__(self, default_platform: str = PC, server_url: str = "https://owapi.net"):
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
                return await func(*args, _session=session, **kwargs)
            else:
                # The session argument wasn't passed, so we create our own
                async with aiohttp.ClientSession() as new_session:
                    return await func(*args, _session=new_session, **kwargs)

        # We return the decorated func
        return decorated_func

    @_uses_aiohttp_session
    async def get_full_profile(self, battletag: str, regions=(EUROPE, KOREA, AMERICAS, CHINA, JAPAN, ANY),
                               platform=None, _session=None):
        """Returns a dictionary where the keys are the regions that there exists and account for, with corresponding values (stats, achievement, heroes).
        The regions argument is an iterable of the regions (see constants.py) that the user wants results for (default all regions). If no matching accounts are found, this returns an empty dict.
        The platforms argument is one of the three platforms in constants.py, and only results from that platforms will be returned, the default is the default of the API instance (see __init__)."""
        if platform is None:
            platform = self.default_platform
        try:
            blob_dict = await self._base_request(battletag, "blob", _session, platform=platform)
        except ValueError as e:
            # The battletag doesn't exist
            blob_dict = {}
        existing_regions = {key: val for key, val in blob_dict.items() if ((val is not None) and (key != "_request"))}
        return {key: val for key, val in existing_regions.items() if key in regions}

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
            params={"platform": platform},  # Passed to _async_get and indicates what platform we're searching on
            headers={"User-Agent": "overwatch_python_api"}
            # According to https://github.com/SunDwarf/OWAPI/blob/master/owapi/v3/v3_util.py#L18 we have to customise our User-Agent, so we do
        )

        # Validate the response
        if status != 200:
            if status == 404 and resp_json["msg"] == "profile not found":
                raise ProfileNotFoundError(
                    "Got HTTP 404, profile not found. This is caused by the given battletag not existing on the specified platform.")
            if status == 429 and resp_json["msg"] == "you are being ratelimited":
                raise RatelimitError(
                    "Got HTTP 429, you are being ratelimited. This is caused by calls to the api too frequently.")
            raise ConnectionError("Did not get HTTP status 200, got: {0}".format(status))
        return resp_json

    async def _async_get(self, session: aiohttp.ClientSession, *args, _async_timeout_seconds: int = 5,
                         **kwargs):
        """Uses aiohttp to make a get request instead of using requests. 
        Will raise asyncio.TimeoutError if the request could not be completed 
        within _async_timeout_seconds (default 5) seconds."""

        # Taken almost directly from the aiohttp tutorial
        with async_timeout.timeout(_async_timeout_seconds):
            async with session.get(*args, **kwargs) as response:
                return await response.json(), response.status
