'''
Goldy Bot Module Package for Nova Universe discord server.
'''
import GoldyBot

AUTHOR = 'Dev Goldy'
AUTHOR_GITHUB = 'https://github.com/NovaUniverse'
OPEN_SOURCE_LINK = 'https://github.com/NovaUniverse/NovaUnivese-GoldyBot-Module'

import staff, mcf

def load():
    # This function get's executed when the module is loaded, so run your extenstion classes in here.
    staff.NovaStaffUtils(package_module_name=__name__)
    mcf.MCF(package_module=__name__)