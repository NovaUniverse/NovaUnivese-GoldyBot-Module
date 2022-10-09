"""
Rewrite of MCF extension.
"""

import os, random

PATH = __path__[0]

class Background_Images():
    def __init__(self):
        pass

    def get_one(self, bg_number:int=1) -> str:
        """Returns a background image from that directory."""
        return PATH + f"/assets/background_{bg_number}.png"

    def get_random(self) -> str:
        return PATH + f"/assets/background_{random.randint(1, len(os.listdir(__path__[0] + '/assets')))}.png"

from .player_cmds import MCFSignup
from .staff_cmds import MCFSignupStaff