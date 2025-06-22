# %%
from pyupdater.client.updates import get_highest_version
from dsdev_utils.helpers import EasyAccessDict
from pathlib import Path
import json

# %%
p = Path('/Users/jayme/Downloads/versions (1)')
with p.open('r') as file:
    data = file.read()

data_json = json.loads(data)
# data_json

# %%

easy_data = EasyAccessDict(data_json)
name = 'SMS Event Log'
plat = 'win'
channel = 'alpha'
get_highest_version(name, plat, channel, easy_data, strict=False)