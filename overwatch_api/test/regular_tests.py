from unittest import TestCase
import vcr
from overwatch_api import OverwatchAPI, PC, AMERICAS, QUICK, heroes


class TestPatchNotes(TestCase):

    def setUp(self):
        self.ow = OverwatchAPI('key')

    @vcr.use_cassette('fixtures/vcr_cassettes/get_patch_notes.yaml')
    def test_get_patch_notes(self):
        result = self.ow.get_patch_notes()
        self.assertIsInstance(result, dict)

    @vcr.use_cassette('fixtures/vcr_cassettes/get_patch_notes.yaml')
    def test_get_patch_notes_keys(self):
        result = self.ow.get_patch_notes()
        self.assertEqual(set(result.keys()), set(['patchNotes', 'pagination']))


class TestUserMethods(TestCase):

    def setUp(self):
        self.ow = OverwatchAPI('key')

    @vcr.use_cassette('fixtures/vcr_cassettes/get_profile.yaml')
    def test_get_profile(self):
        result = self.ow.get_profile(PC, AMERICAS, 'elyK-1940')
        self.assertIsInstance(result, dict)

    @vcr.use_cassette('fixtures/vcr_cassettes/get_profile.yaml')
    def test_get_profile_keys(self):
        result = self.ow.get_profile(PC, AMERICAS, 'elyK-1940')
        self.assertIn('data', result.keys())

    @vcr.use_cassette('fixtures/vcr_cassettes/get_achievements.yaml')
    def test_get_user_achievements(self):
        result = self.ow.get_achievements(PC, AMERICAS, 'elyK-1940')
        self.assertIsInstance(result, dict)

    @vcr.use_cassette('fixtures/vcr_cassettes/get_achievements.yaml')
    def test_get_user_achievements_keys(self):
        result = self.ow.get_achievements(PC, AMERICAS, 'elyK-1940')
        expected_keys = set(['totalNumberOfAchievements',
                             'numberOfAchievementsCompleted',
                             'finishedAchievements', 'achievements'])
        self.assertEqual(set(result.keys()), expected_keys)

    @vcr.use_cassette('fixtures/vcr_cassettes/get_stats_all_heroes.yaml')
    def test_get_stats_all_heroes(self):
        result = self.ow.get_stats_all_heroes(PC, AMERICAS, 'elyK-1940', QUICK)
        self.assertIsInstance(result, dict)

    @vcr.use_cassette('fixtures/vcr_cassettes/get_stats_all_heroes.yaml')
    def test_get_stats_all_heroes_keys(self):
        result = self.ow.get_stats_all_heroes(PC, AMERICAS, 'elyK-1940', QUICK)
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
    def test_get_stats_one_hero(self):
        result = self.ow.get_stats_selected_heroes(PC, AMERICAS, 'elyK-1940', QUICK,
                                                   [heroes['MERCY']])
        self.assertIsInstance(result, dict)

    @vcr.use_cassette('fixtures/vcr_cassettes/get_stats_one_hero.yaml')
    def test_get_stats_one_hero_keys(self):
        result = self.ow.get_stats_selected_heroes(PC, AMERICAS, 'elyK-1940',
                                                   QUICK, [heroes['MERCY']])
        print(result)
        self.assertIn('Mercy', result.keys())
        self.assertIn('PlayersResurrected', result['Mercy'].keys())

    @vcr.use_cassette('fixtures/vcr_cassettes/get_stats.yaml')
    def test_get_stats(self):
        result = self.ow.get_stats_heroes_used(PC, AMERICAS, 'elyK-1940', QUICK)
        self.assertIsInstance(result, list)

    @vcr.use_cassette('fixtures/vcr_cassettes/get_stats.yaml')
    def test_get_stats_amount(self):
        result = self.ow.get_stats_heroes_used(PC, AMERICAS, 'elyK-1940', QUICK)
        self.assertEqual(len(result), len(heroes))
