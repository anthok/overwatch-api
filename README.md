# overwatch-api
Python Overwatch API

## Install

    pip install overwatch-api


### [0.5.0] - 2017-04-21
#### Changes
- Now using Async, thanks @Drummersbrother!
- Moving API provider to OWAPI, thanks @Drummersbrother!


## Example Code - Supported calls
A segment from example_test.py, which can provide more info on how to use the API.
``` python
from overwatch_api.core import AsyncOWAPI
from overwatch_api.constants import *

client = AsyncOWAPI()
client.get_profile("Danielfrogs#2552", session=session, platform=PC)
client.get_stats("Danielfrogs#2552", session=session, platform=PC)
client.get_achievements("Danielfrogs#2552", session=session, platform=PC)
client.get_hero_stats("Danielfrogs#2552", session=session, platform=PC)
```


## Testing (Not working in 0.5 yet!)

``` bash
    python setup.py test
```

## Deprecated Calls (0.4 and below)
``` python
from overwatch_api import *

ow = OverwatchAPI()

ow.get_patch_notes()
ow.get_achievements(PC,AMERICAS,'elyK-1940')
ow.get_platforms(PC,AMERICAS,'elyK-1940')
ow.get_profile(PC,AMERICAS,'elyK-1940')
ow.get_stats_all_heroes(PC,AMERICAS,'elyK-1940',COMP)
ow.get_stats_selected_heroes(PC,AMERICAS,'elyK-1940',COMP,[heroes['MERCY'],heroes['LUCIO']])
ow.get_stats_heroes_used(PC,AMERICAS,'elyK-1940',COMP)
```



