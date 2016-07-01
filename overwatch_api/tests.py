from overwatch_api import *

ow = OverwatchAPI('key')

ow.get_patch_notes()
print ('Patch notes passed')

ow.get_user_achievements(PC,AMERICAS,'elyK-1940')
print ('User achievements passed')

ow.get_stats_all_heroes(PC,AMERICAS,'elyK-1940',QUICK)
print ('Stats all heroes passed')

ow.get_stats_one_hero(PC,AMERICAS,'elyK-1940',QUICK,heroes['MERCY'])
print ('Stats one hero passed')

ow.get_stats(PC,AMERICAS,'elyK-1940',QUICK)
print ('Player stats passed')

ow.get_profile(PC,AMERICAS,'elyK-1940')
print ('User profile passed')
