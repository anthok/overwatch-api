import asyncio

import aiohttp
import async_timeout

from overwatch_api.constants import *
from overwatch_api.exceptions import *

"""The async interface to the OWAPI (https://github.com/SunDwarf/OWAPI) api."""


# TODO Handle being ratelimited, asyncio.sleep?

class AsyncOWAPI(object):
    """The async client objeWct to use when you want to use the OWAPI api.
    All requests throw ConnectionError if they can't connect or similar problem.
    Other exceptions should be reported as bugs if they're raised."""

    def __init__(self, default_platform: str = PC, server_url: str = "https://owapi.net", *,
                 handle_ratelimit: bool = True, max_tries: int = 3, request_timeout: float = 5):
        """Creates and sets up the client object.
        default_platform is one of PC, PLAYSTATION, or XBOX, from constants.py. 
            It specifies what platform the api should default to search on if no platform parameter is supplied to a method.
        server_url is the url (or aiohttp compatible address) to the OWAPI server.
        handle_ratelimit specifies whether the api should retry when a request gets ratelimited.
        max_tries is the maximum number of tries to retry when a request gets ratelimited, only applicable if handle_ratelimit is True.
        request_timeout is the timeout to use for each individual request to the API in seconds.
        """

        # Stuff the user should have control over
        self.server_url = server_url
        self.default_platform = default_platform

        # Optional client parameters
        # If ratelimiting should be handled
        self.default_handle_ratelimit = handle_ratelimit
        # The max number of tries to do until a Ratelimit exception is raised
        self.default_max_tries = max_tries
        # The timeout to use on each request
        self.default_request_timeout = request_timeout

        # If you're an advanced user you maybe, sometime, idk, probably, might want to control these
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

    def _add_request_parameters(func):
        """Adds the ratelimit and request timeout parameters to a function."""

        # The function the decorator returns
        async def decorated_func(*args, handle_ratelimit=None, max_tries=None, request_timeout=None, **kwargs):
            return await func(*args, handle_ratelimit=handle_ratelimit, max_tries=max_tries,
                              request_timeout=request_timeout, **kwargs)

        # We return the decorated func
        return decorated_func

    @_uses_aiohttp_session
    @_add_request_parameters
    async def get_profile(self, battletag: str, regions=(EUROPE, KOREA, AMERICAS, CHINA, JAPAN, ANY),
                          platform=None, _session=None, handle_ratelimit=None, max_tries=None, request_timeout=None):
        """Returns a dictionary where the keys are the regions that there exists an account for, with corresponding values (stats, achievement, heroes).
        The regions argument is an iterable of the regions (see constants.py) that the user wants results for (default all regions). If no matching accounts are found for the platform and regions, this returns an empty dict.
        The platforms argument is one of the three platforms in constants.py, and only results from that platforms will be returned, the default is the default of the API instance (see __init__)."""
        if platform is None:
            platform = self.default_platform
        try:
            blob_dict = await self._base_request(battletag, "blob", _session, platform=platform,
                                                 handle_ratelimit=handle_ratelimit, max_tries=max_tries,
                                                 request_timeout=request_timeout)
        except ProfileNotFoundError as e:
            # The battletag doesn't exist
            blob_dict = {}
        existing_regions = {key: val for key, val in blob_dict.items() if ((val is not None) and (key != "_request"))}
        return {key: val for key, val in existing_regions.items() if key in regions}

    @_uses_aiohttp_session
    @_add_request_parameters
    async def get_stats(self, battletag: str, regions=(EUROPE, KOREA, AMERICAS, CHINA, JAPAN, ANY),
                        platform=None, _session=None, handle_ratelimit=None, max_tries=None, request_timeout=None):
        """Returns the stats for the profiles on the specified regions and platform. The format for regions without a matching user, the format is the same as get_profile.
        The stats are returned in a dictionary with a similar format to what https://github.com/SunDwarf/OWAPI/blob/master/api.md#get-apiv3ubattletagstats specifies."""

        if platform is None:
            platform = self.default_platform
        try:
            blob_dict = await self._base_request(battletag, "stats", _session, platform=platform,
                                                 handle_ratelimit=handle_ratelimit, max_tries=max_tries,
                                                 request_timeout=request_timeout)
        except ProfileNotFoundError as e:
            # The battletag doesn't exist
            blob_dict = {}
        existing_regions = {key: val for key, val in blob_dict.items() if ((val is not None) and (key != "_request"))}
        return {key: [inner_val for inner_key, inner_val in val.items() if inner_key == "stats"][0] for key, val in
                existing_regions.items() if key in regions}

    @_uses_aiohttp_session
    @_add_request_parameters
    async def get_achievements(self, battletag: str, regions=(EUROPE, KOREA, AMERICAS, CHINA, JAPAN, ANY),
                               platform=None, _session=None, handle_ratelimit=None, max_tries=None,
                               request_timeout=None):
        """Returns the achievements for the profiles on the specified regions and platform. Does not return keys for regions that don't have a matching user, the format is the same as get_profile.
        The achievements are returned in a dictionary with a similar format to what https://github.com/SunDwarf/OWAPI/blob/master/api.md#get-apiv3ubattletagachievements specifies."""

        if platform is None:
            platform = self.default_platform
        try:
            blob_dict = await self._base_request(battletag, "achievements", _session, platform=platform,
                                                 handle_ratelimit=handle_ratelimit, max_tries=max_tries,
                                                 request_timeout=request_timeout)
        except ProfileNotFoundError as e:
            # The battletag doesn't exist
            blob_dict = {}
        existing_regions = {key: val for key, val in blob_dict.items() if ((val is not None) and (key != "_request"))}
        return {key: [inner_val for inner_key, inner_val in val.items() if inner_key == "achievements"][0] for key, val
                in existing_regions.items() if key in regions}

    @_uses_aiohttp_session
    @_add_request_parameters
    async def get_hero_stats(self, battletag: str, regions=(EUROPE, KOREA, AMERICAS, CHINA, JAPAN, ANY),
                             platform=None, _session=None, handle_ratelimit=None, max_tries=None, request_timeout=None):
        """Returns the hero stats for the profiles on the specified regions and platform. Does not return keys for regions that don't have a matching user, the format is the same as get_profile.
        The hero stats are returned in a dictionary with a similar format to what https://github.com/SunDwarf/OWAPI/blob/master/api.md#get-apiv3ubattletagheroes specifies."""

        if platform is None:
            platform = self.default_platform
        try:
            blob_dict = await self._base_request(battletag, "heroes", _session, platform=platform,
                                                 handle_ratelimit=handle_ratelimit, max_tries=max_tries,
                                                 request_timeout=request_timeout)
        except ProfileNotFoundError as e:
            # The battletag doesn't exist
            blob_dict = {}
        existing_regions = {key: val for key, val in blob_dict.items() if ((val is not None) and (key != "_request"))}
        return {key: [inner_val for inner_key, inner_val in val.items() if inner_key == "heroes"][0] for key, val in
                existing_regions.items() if key in regions}

    @staticmethod
    def sanitize_battletag(battle_tag: str) -> str:
        """In the api, battletags' #:s are replaced with dashes, this method does that."""
        if "#" in battle_tag:
            battle_tag = battle_tag.replace("#", "-")
        return battle_tag

    async def _base_request(self, battle_tag: str, endpoint_name: str, session: aiohttp.ClientSession, *, platform=None,
                            handle_ratelimit=None, max_tries=None, request_timeout=None):
        """Does a request to some endpoint. This is also where ratelimit logic is handled."""
        # We check the different optional arguments, and if they're not passed (are none) we set them to the default for the client object
        if platform is None:
            platform = self.default_platform
        if handle_ratelimit is None:
            handle_ratelimit = self.default_handle_ratelimit
        if max_tries is None:
            max_tries = self.default_max_tries
        if request_timeout is None:
            request_timeout = self.default_request_timeout

        # The battletag with #s removed
        san_battle_tag = self.sanitize_battletag(battle_tag)

        # The ratelimit logic
        for _ in range(max_tries):
            # We execute a request
            try:
                resp_json, status = await self._async_get(
                    session,
                    self.server_url + self._api_urlpath + "{battle_tag}/{endpoint}".format(
                        battle_tag=san_battle_tag,
                        endpoint=endpoint_name
                    ),
                    params={"platform": platform},
                    # Passed to _async_get and indicates what platform we're searching on
                    headers={"User-Agent": "overwatch_python_api"},
                    # According to https://github.com/SunDwarf/OWAPI/blob/master/owapi/v3/v3_util.py#L18 we have to customise our User-Agent, so we do
                    _async_timeout_seconds=request_timeout
                )
                if status == 429 and resp_json["msg"] == "you are being ratelimited":
                    raise RatelimitError
            except RatelimitError as e:
                # This excepts both RatelimitErrors and TimeoutErrors, ratelimiterrors for server returning a ratelimit, timeouterrors for the connection not being done in with in the timeout
                # We are ratelimited, so we check if we handle ratelimiting logic
                # If so, we wait and then execute the next iteration of the loop
                if handle_ratelimit:
                    # We wait to remedy ratelimiting, and we wait a bit more than the response says we should
                    await asyncio.sleep(resp_json["retry"] + 1)
                    continue
                else:
                    raise
            else:
                # We didn't get an error, so we exit the loop because it was a successful request
                break
        else:
            # The loop didn't stop because it got breaked, which means that we got ratelimited until the maximum number of tries were finished
            raise RatelimitError("Got ratelimited for each requests until the maximum number of retries were reached.")

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
        """Uses aiohttp to make a get request asynchronously. 
        Will raise asyncio.TimeoutError if the request could not be completed 
        within _async_timeout_seconds (default 5) seconds."""

        # Taken almost directly from the aiohttp tutorial
        with async_timeout.timeout(_async_timeout_seconds):
            async with session.get(*args, **kwargs) as response:
                return await response.json(), response.status
