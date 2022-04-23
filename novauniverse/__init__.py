'''
Goldy Bot Module for Nova Universe discord server.
'''
import GoldyBot

AUTHOR = 'Dev Goldy'
AUTHOR_GITHUB = 'https://github.com/NovaUniverse'
OPEN_SOURCE_LINK = 'https://github.com/NovaUniverse/NovaUnivese-GoldyBot-Module'

import staff

def load():
    # This function get's executed when the module is loaded, so run your extenstion classes in here.
    
    staff.NovaStaffUtils(package_module_name=__name__)