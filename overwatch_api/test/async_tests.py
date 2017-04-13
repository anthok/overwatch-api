import vcr
import asyncio
import unittest
from overwatch_api import PC, AMERICAS, QUICK, heroes
from overwatch_api.overwatch_api_async import Async_OverwatchAPI as OverwatchAPI

class AioTestCase(unittest.TestCase):
    """We need to test async code, this was shamelessly taken from 
    http://stackoverflow.com/questions/23033939/how-to-test-python-3-4-asyncio-code"""
    def __init__(self, methodName='runTest', loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self._function_cache = {}
        super(AioTestCase, self).__init__(methodName=methodName)
    
    def coroutine_function_decorator(self, func):
        def wrapper(*args, **kw):
            return self.loop.run_until_complete(func(*args, **kw))
        return wrapper
    
    def __getattribute__(self, item):
        attr = object.__getattribute__(self, item)
        if asyncio.iscoroutinefunction(attr):
            if item not in self._function_cache:
                self._function_cache[item] = self.coroutine_function_decorator(attr)
            return self._function_cache[item]
        return attr

class aioTestPatchNotes(AioTestCase):

    def setUp(self):
        self.ow = OverwatchAPI('key')
    
    @vcr.use_cassette('fixtures/vcr_cassettes/get_patch_notes.yaml')
    async def test_get_patch_notes(self):
        result = await self.ow.get_patch_notes()
        self.assertIsInstance(result, dict)
            
    @vcr.use_cassette('fixtures/vcr_cassettes/get_patch_notes.yaml')
    async def test_get_patch_notes_keys(self):
        result = await itself.ow.get_patch_notes()
        itself.assertEqual(set(result.keys()), set(['patchNotes', 'pagination']))

class TestUserMethods(AioTestCase):

    def setUp(self):
        self.ow = OverwatchAPI('key')
    
    @vcr.use_cassette('fixtures/vcr_cassettes/get_profile.yaml')
    async def test_get_profile(self):
        result = await self.ow.get_profile(PC, AMERICAS, 'elyK-1940')
        self.assertIsInstance(result, dict)
    
    @vcr.use_cassette('fixtures/vcr_cassettes/get_profile.yaml')
    async def test_get_profile_keys(self):
        result = await self.ow.get_profile(PC, AMERICAS, 'elyK-1940')
        self.assertIn('data', result.keys())
    
    @vcr.use_cassette('fixtures/vcr_cassettes/get_achievements.yaml')
    async def test_get_user_achievements(self):
        result = await self.ow.get_achievements(PC, AMERICAS, 'elyK-1940')
        self.assertIsInstance(result, dict)
    
    @vcr.use_cassette('fixtures/vcr_cassettes/get_achievements.yaml')
    async def test_get_user_achievements_keys(self):
        result = await self.ow.get_achievements(PC, AMERICAS, 'elyK-1940')
        expected_keys = set(['totalNumberOfAchievements',
                             'numberOfAchievementsCompleted',
                             'finishedAchievements', 'achievements'])
        self.assertEqual(set(result.keys()), expected_keys)
    
    @vcr.use_cassette('fixtures/vcr_cassettes/get_stats_all_heroes.yaml')
    async def test_get_stats_all_heroes(self):
        result = await self.ow.get_stats_all_heroes(PC, AMERICAS, 'elyK-1940', QUICK)
        self.assertIsInstance(result, dict)
    
    @vcr.use_cassette('fixtures/vcr_cassettes/get_stats_all_heroes.yaml')
    async def test_get_stats_all_heroes_keys(self):
        result = await self.ow.get_stats_all_heroes(PC, AMERICAS, 'elyK-1940', QUICK)
        expected_keys = set(['MeleeFinalBlow',
                             'SoloKills',
                             'ObjectiveKills',
                             'FinalBlows',
                             'DamageDone',
                             'Eliminations',
                             'EnvironmentalKills',
                             'Multikills',
                             'HealingDone',
                             'ReconAssists',
                             'TeleporterPadDestroyed',
                             'Eliminations-MostinGame',
                             'FinalBlows-MostinGame',
                             'DamageDone-MostinGame',
                             'HealingDone-MostinGame',
                             'DefensiveAssists-MostinGame',
                             'OffensiveAssists-MostinGame',
                             'ObjectiveKills-MostinGame',
                             'ObjectiveTime-MostinGame',
                             'Multikill-Best',
                             'SoloKills-MostinGame',
                             'TimeSpentonFire-MostinGame',
                             'MeleeFinalBlows-Average',
                             'TimeSpentonFire-Average',
                             'SoloKills-Average',
                             'ObjectiveTime-Average',
                             'ObjectiveKills-Average',
                             'HealingDone-Average',
                             'FinalBlows-Average',
                             'Deaths-Average',
                             'DamageDone-Average',
                             'Eliminations-Average',
                             'Deaths',
                             'EnvironmentalDeaths',
                             'Cards',
                             'Medals',
                             'Medals-Gold',
                             'Medals-Silver',
                             'Medals-Bronze',
                             'GamesWon',
                             'TimeSpentonFire',
                             'ObjectiveTime',
                             'TimePlayed',
                             'MeleeFinalBlow-MostinGame',
                             'ReconAssists-Average',
                             'DefensiveAssists',
                             'DefensiveAssists-Average',
                             'OffensiveAssists',
                             'OffensiveAssists-Average'])
        self.assertEqual(set(result.keys()), expected_keys)
    
    @vcr.use_cassette('fixtures/vcr_cassettes/get_stats_one_hero.yaml')
    async def test_get_stats_one_hero(self):
        result = await self.ow.get_stats_selected_heroes(PC, AMERICAS, 'elyK-1940', QUICK,
                                                   [heroes['MERCY']])
        self.assertIsInstance(result, dict)
    
    @vcr.use_cassette('fixtures/vcr_cassettes/get_stats_one_hero.yaml')
    async def test_get_stats_one_hero_keys(self):
        result = await self.ow.get_stats_selected_heroes(PC, AMERICAS, 'elyK-1940',
                                                   QUICK, [heroes['MERCY']])
        self.assertIn('Mercy', result.keys())
        self.assertIn('PlayersResurrected', result['Mercy'].keys())
    
    @vcr.use_cassette('fixtures/vcr_cassettes/get_stats.yaml')
    async def test_get_stats(self):
        result = await self.ow.get_stats_heroes_used(PC, AMERICAS, 'elyK-1940', QUICK)
        self.assertIsInstance(result, list)
    
    @vcr.use_cassette('fixtures/vcr_cassettes/get_stats.yaml')
    async def test_get_stats_amount(self):
        result = await self.ow.get_stats_heroes_used(PC, AMERICAS, 'elyK-1940', QUICK)
        self.assertEqual(len(result), len(heroes))
