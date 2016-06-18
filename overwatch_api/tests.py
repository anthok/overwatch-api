from overwatch_api import *

ow = OverwatchAPI('key')

ow.get_patch_notes()
ow.get_user_achievements(PC,AMERICAS,'elyK-1940')
ow.get_stats_all_heroes(PC,AMERICAS,'elyK-1940')
ow.get_stats_one_hero(PC,AMERICAS,'elyK-1940',heroes['MERCY'])
ow.get_stats(PC,AMERICAS,'elyK-1940')
ow.get_profile(PC,AMERICAS,'elyK-1940')
