# overwatch-api
Python Overwatch API

A Lootbox.eu wrapper

## Install

    pip install overwatch-api

## Example Code

    python -m unittest -v tests.py

## Supported calls

    from overwatch_api import *
    ow = OverwatchAPI('key')
    ow.get_patch_notes()
    ow.get_achievements(PC,AMERICAS,'elyK-1940')
    ow.get_platforms(PC,AMERICAS,'elyK-1940')
    ow.get_profile(PC,AMERICAS,'elyK-1940')
    ow.get_stats_all_heroes(PC,AMERICAS,'elyK-1940',COMP)
    ow.get_stats_selected_heroes(PC,AMERICAS,'elyK-1940',COMP,[heroes['MERCY'],heroes['LUCIO']])
    ow.get_stats_heroes_used(PC,AMERICAS,'elyK-1940',COMP)
