import requests

#REGIONS
AMERICAS = 'us'
EUROPE = 'eu'
KOREA = 'kr'
CHINA = 'cn'
JAPAN = 'jp'
GLOBAL = 'global'

#PLATFORMS
PC = 'pc'
XBOX = 'xbl'
PLAYSTATION = 'psn'

heroes = {
    'BASTION': 'Bastion',
    'DIVA': 'D.Va',
    'GENJI': 'Genji',
    'HANZO': 'Hanzo',
    'JUNKRAT': 'Junkrat',
    'LUCIO': 'Lúcio',
    'MCCREE': 'McCree',
    'MEI': 'Mei',
    'MERCY': 'Mercy',
    'PHARAH': 'Pharah',
    'REAPER': 'Reaper',
    'REINHARDT': 'Reinhardt',
    'ROADHOG': 'Roadhog',
    'SOLDIER_76': 'Soldier: 76',
    'SYMMETRA': 'Symmetra',
    'TORBJORN': 'Torbjörn',
    'TRACER': 'Tracer',
    'WIDOWMAKER': 'Widowmaker',
    'WINSTON': 'Winston',
    'ZARYA': 'Zarya',
    'ZENYATTA': 'Zenyatta'
}


'''
Future proofing, as it is likely that a key
will be required in the future
'''
class OverwatchAPI:
    def __init__(self,key,default_plaform=PC,default_region=AMERICAS):
        self.key = key
        self.default_plaform = default_plaform
        self.default_region = default_region

    def get_patch_notes(self):
        r = requests.get('https://api.lootbox.eu/patch_notes')
        self.validate_response(r)
        return r.json()

    def get_user_achievements(self,platform,region,battle_tag):
        return self._base_request(
            platform,region,battle_tag,
            'achievements'
        )

    def get_stats_all_heroes(self,platform,region,battle_tag):
        return self._base_request(
            platform,region,battle_tag,
            'allHeroes/'
        )

    def get_stats_one_hero(self,platform,region,battle_tag,hero):
        return self._base_request(
            platform,region,battle_tag,
            'hero/' + hero
        )

    def get_stats(self,platform,region,battle_tag):
        return self._base_request(
            platform,region,battle_tag,
            'heroes'
        )

    def get_profile(self,platform,region,battle_tag):
        return self._base_request(
            platform,region,battle_tag,
            'profile'
        )

    def validate_response(self,response):
        if response.status_code != 200:
            raise Exception

    def sanitize_battletag(self,battle_tag):
        if '#' in battle_tag:
            battle_tag = battle_tag.replace('#','-')
        return battle_tag

    def _base_request(self,platform,region,battle_tag,url):
        if region is None:
            region = self.default_region
        if platform is None:
            platform = self.default_plaform

        battle_tag = self.sanitize_battletag(battle_tag)

        r = requests.get(
            'https://api.lootbox.eu/{platform}/{region}/{battle_tag}/{url}'.format(
                platform=platform,
                region=region,
                battle_tag=battle_tag,
                url=url
                )
            )

        self.validate_response(r)
        return r.json()
