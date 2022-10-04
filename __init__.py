'''
Goldy Bot Module Package for Nova Universe discord server.
'''
import GoldyBot

AUTHOR = 'Dev Goldy'
AUTHOR_GITHUB = 'https://github.com/NovaUniverse'
OPEN_SOURCE_LINK = 'https://github.com/NovaUniverse/novacord'
VERSION = 1.1

import errors
import staff, mcf, mcf_signup

def load():
    # This function get's executed when the module is loaded, so run your extension classes in here.
    staff.NovaStaffUtils(package_module_name=__name__)
    #mcf.MCF(package_module=__name__)

    #  MCF Sign Up System
    #==============================
    # Loading it's extensions.
    mcf_signup.MCFSignup(__name__)
    mcf_signup.MCFSignupStaff(__name__)