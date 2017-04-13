import aiohttp
import async_timeout
from .utilities import *

'''
Future proofing, as it is likely that a key
will be required in the future
'''


class Async_OverwatchAPI:
    """An alternate, async version of the OverwatchAPI class. This requires python => 3.5, 
    as it uses async def and await. Also requires aiohttp and async_timeout."""

    def __init__(self, key=None, default_plaform=PC, default_region=AMERICAS, default_mode=QUICK):
        self.key = key
        self.default_plaform = default_plaform
        self.default_region = default_region
        self.default_mode = default_mode

    async def get_patch_notes(self):
        r = self._async_get('https://api.lootbox.eu/patch_notes')
        self.validate_response(r)
        return await r.json()

    async def get_achievements(self, platform, region, battle_tag, mode=None):
        return await self._base_request(
            platform, region, battle_tag, mode,
            'achievements'
        )

    async def get_platforms(self, platform, region, battle_tag, mode=None):
        return await self._base_request(
            platform, region, battle_tag, mode,
            'get-platforms'
        )

    async def get_profile(self, platform, region, battle_tag, mode=None):
        return await self._base_request(
            platform, region, battle_tag, mode,
            'profile'
        )

    async def get_stats_all_heroes(self, platform, region, battle_tag, mode):
        return await self._base_request(
            platform, region, battle_tag, mode,
            'allHeroes/'
        )

    async def get_stats_selected_heroes(self, platform, region, battle_tag, mode, heroes):
        # url encode for comma
        heroes = '%2C'.join(heroes)

        return await self._base_request(
            platform, region, battle_tag, mode,
            'hero/' + heroes + '/'
        )

    async def get_stats_heroes_used(self, platform, region, battle_tag, mode):
        return await self._base_request(
            platform, region, battle_tag, mode,
            'heroes'
        )

    def validate_response(self, response):
        if response.status != 200:
            raise Exception

    def sanitize_battletag(self, battle_tag):
        if '#' in battle_tag:
            battle_tag = battle_tag.replace('#', '-')
        return battle_tag

    async def _base_request(self, platform, region, battle_tag, mode, url):
        if region is None:
            region = self.default_region
        if platform is None:
            platform = self.default_plaform

        battle_tag = self.sanitize_battletag(battle_tag)
        if mode is None:
            r = await self._async_get(
                'https://api.lootbox.eu/{platform}/{region}/{battle_tag}/{url}'.format(
                    platform=platform,
                    region=region,
                    battle_tag=battle_tag,
                    url=url
                )
            )
        else:
            r = await self._async_get(
                'https://api.lootbox.eu/{platform}/{region}/{battle_tag}/{mode}/{url}'.format(
                    platform=platform,
                    region=region,
                    battle_tag=battle_tag,
                    mode=mode,
                    url=url
                )
            )

        self.validate_response(r)
        return await r.json()

    async def _async_get(_async_timeout_seconds=5, *args, **kwargs):
        """Uses aiohttp to make a get request instead of using requests. 
        Will raise asyncio.TimeoutError if the request could not be completed 
        within _async_timeout_seconds (default 5) seconds."""
        
        # Taken almost directly from the aiohttp tutorial
        with async_timeout.timeout(_async_timeout_seconds):
            async with session.get(*args, **kwargs) as response:
                return await response
