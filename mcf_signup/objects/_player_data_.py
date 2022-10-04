from __future__ import annotations

import GoldyBot
from datetime import datetime

import novauniverse

class PlayerData():
    """Class containing all info to add a player to a tournament."""
    def __init__(self, member:GoldyBot.Member, mc_ign:str, team:str, pending_teammate:GoldyBot.Member):
        self.member_ = member
        self.mc_ign_ = mc_ign
        self.team_ = team
        self.pending_teammate_member_object_ = pending_teammate

    @property
    def member(self):
        return self.member_

    @property
    def mc_ign(self) -> str:
        return self.mc_ign_

    @property
    def mc_uuid(self):
        return novauniverse._find_.player_name_to_uuid(self.mc_ign)

    @property
    def team(self):
        return self.team_

    @property
    def pending_teammate(self):
        return self.pending_teammate_member_object_