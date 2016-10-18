# overwatch-api
Python Overwatch API

A Lootbox.eu wrapper

## Install

    pip install overwatch-api
    
## Example Code

    python -m unittests -v tests.py

## Supported calls

    ow.get_patch_notes()
    ow.get_user_achievements(PC,AMERICAS,'elyK-1940')
    ow.get_stats_all_heroes(PC,AMERICAS,'elyK-1940',QUICK)
    ow.get_stats_one_hero(PC,AMERICAS,'elyK-1940',QUICK,heroes['MERCY'])
    ow.get_stats(PC,AMERICAS,'elyK-1940',QUICK)
    ow.get_profile(PC,AMERICAS,'elyK-1940')
