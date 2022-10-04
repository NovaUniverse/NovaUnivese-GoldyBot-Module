import asyncio
import os
import random as random_
from typing import Dict, List, Tuple
import GoldyBot
import json

from GoldyBot.utility.datetime import *

class Background_Images():
    def __init__(self):
        pass

    def get_one(self, bg_number:int=1):
        """Returns a backgrounud image from that directory."""
        return f"/assets/background_{bg_number}.png"

    def get_random(self):
        return __path__[0] + f"/assets/background_{random_.randint(1, len(os.listdir(__path__[0] + '/assets')))}.png"

from . import _forms_, _info_, _tournament_, _player_

from GoldyBot.utility.datetime.user_input import *
from GoldyBot.utility.commands import *

class MCF(GoldyBot.Extension):
    def __init__(self, package_module=None):
        super().__init__(self, package_module_name=package_module)

        self.tournament:_tournament_.MCFTournament = None

        # Embeds
        #==========
        self.form_closed = GoldyBot.utility.goldy.embed.Embed(
            title="🔒 The form is now closed!",
            description=f"""
            ❌ *You can no longer join or leave the tournament. If you would like to do any of those please contact staff.*
            """,
            colour=GoldyBot.utility.goldy.colours.AKI_ORANGE
        )

        self.no_mcf_embed = GoldyBot.utility.goldy.embed.Embed(
            title="⛔ SignUps not open yet!",
            description=f"""
            ❌ *Sorry we haven't open signups for the next mcf yet.*
            """,
            colour=GoldyBot.utility.goldy.colours.AKI_RED
        )

        self.youve_been_removed_embed = GoldyBot.utility.goldy.embed.Embed(
            title="🧳 You've been removed!",
            description=f"""
            🚚 You've been removed from this week's mcf.
            """,
            colour=GoldyBot.utility.goldy.colours.WHITE
        )

        self.your_already_registered_embed = GoldyBot.utility.goldy.embed.Embed(
            title="💚 Your already in! 😊",
            description=f"""
            ✔ Your already registered for this week's mcf.
            """,
            colour=GoldyBot.utility.goldy.colours.GREEN,
        )
        self.your_already_registered_embed.footer.text = "(Notice: Just a reminder that this doesn't mean your actually confirmed to be playing.)"

        self.your_not_in_this_weeks_mcf_embed = GoldyBot.utility.goldy.embed.Embed(
            title="❤ Your not in this weeks mcf!",
            description=f"""
            ⚠ Your not registered for this week's mcf.
            """,
            colour=GoldyBot.utility.goldy.colours.RED
        )

    def loader(self):
        @GoldyBot.command(slash_cmd_only=True)
        async def mcf(self:MCF, ctx:GoldyBot.objects.slash.InteractionToCtx):
            self.tournament = await _info_.TournamentInfo().get_latest_mcf()

            if not self.tournament == None:
                return True # Your good to continue to the sub command.

            else:
                # No mcf available.
                message = await send(ctx, embed=self.no_mcf_embed)

                await asyncio.sleep(20)

                await message.delete()

                # Stop right here! Don't continue!
                return False

        @mcf.sub_command(help_des="An amazing command to sign up for the mcf minecraft tournament right from the comfort of Discord.")
        async def join(self:MCF, ctx:GoldyBot.objects.slash.InteractionToCtx):
            if await self.tournament.is_form_open():
                if not await self.tournament.is_member_registered(GoldyBot.Member(ctx)):
                    await ctx.send_modal(_forms_.JoinMCFForm(self.tournament))
                else:
                    # Your already in!
                    message = await send(ctx, embed=self.your_already_registered_embed)

                    await asyncio.sleep(15)

                    await message.delete()
            else:
                message = await send(ctx, embed=self.form_closed)

                await asyncio.sleep(20)

                await message.delete()

        @mcf.sub_command(help_des="A command for players to leave this week's mcf tournament.")
        async def leave(self:MCF, ctx:GoldyBot.objects.slash.InteractionToCtx):
            member = GoldyBot.Member(ctx)
            
            if await self.tournament.is_form_open():
                # Check if player is registered.
                if await self.tournament.is_member_registered(member):
                    # If registered remove the player.
                    await self.tournament.remove_player(await self.tournament.get_player(member))
                    await send(ctx, embed=self.youve_been_removed_embed)

                else:
                    message = await send(ctx, embed=self.your_not_in_this_weeks_mcf_embed)

                    await asyncio.sleep(15)

                    await message.delete()

            else:
                message = await send(ctx, embed=self.form_closed)

                await asyncio.sleep(20)

                await message.delete()

        @mcf.sub_command(help_des="A command that allows you to team up with a friend for the mcf.")
        async def team(self:MCF, ctx:GoldyBot.objects.slash.InteractionToCtx):
            if await self.tournament.is_form_open():
                member = GoldyBot.Member(ctx)

                if await self.tournament.is_member_registered(member):
                    player_list = []

                    for player_doc in await self.tournament.tournament_database.find_all(user_output.make_date_human(self.tournament.date)):
                        if not player_doc["_id"] == 0:
                            if not player_doc["_id"] == member.member_id:
                                player_list.append(_player_.MCFPlayer(ctx, player_doc["mc_ign"], player_doc["team"], player_doc["pending_teammate"], player_doc["_id"]))

                    view = _forms_.MCFTeamPlayersDropdownView(GoldyBot.Member(ctx), player_list)

                    message = await send(ctx, embed=GoldyBot.utility.goldy.embed.Embed(
                        title="🔥 Who would you like to team with?",
                        description="**🐱‍🏍 Pick a player.**",
                        colour=GoldyBot.utility.goldy.colours.WHITE
                    ), view=view)

                    await asyncio.sleep(60)
                    await message.delete()
                else:
                    message = await send(ctx, embed=self.your_not_in_this_weeks_mcf_embed)
                    await asyncio.sleep(15)
                    await message.delete()

            else:
                embed = self.form_closed
                embed.description += "\n\n *If you would like to team with a player, contact staff immediately.*"
                message = await send(ctx, embed=embed)

                await asyncio.sleep(20)

                await message.delete()

        @mcf.sub_command(help_des="Admin command to create an mcf tournament.", required_roles=["nova_admin"], also_run_parent_CMD=False)
        async def create(self:MCF, ctx:GoldyBot.objects.slash.InteractionToCtx):
            await ctx.send_modal(_forms_.CreateMCFForm())

        @mcf.sub_command(help_des="Admin command to open the mcf form.", required_roles=["nova_admin"], also_run_parent_CMD=False)
        async def open_form(self:MCF, ctx:GoldyBot.objects.slash.InteractionToCtx):
            tournament_info = _info_.TournamentInfo()

            mcf = await tournament_info.get_latest_mcf()
            if not mcf == None:
                if await mcf.open_form():
                    await send(ctx, embed=GoldyBot.utility.goldy.embed.Embed(
                        title="🎉 Form Open!",
                        description="**🎊 The signup form for mcf is open!**",
                        colour=GoldyBot.utility.goldy.colours.PURPLE
                    ))

            else:
                await send(ctx, embed=GoldyBot.utility.goldy.embed.Embed(
                    title="⛔ No MCF!",
                    description="**🛑 There's no mcf being hosted!**",
                    colour=GoldyBot.utility.goldy.colours.AKI_RED
                ))
                

        @mcf.sub_command(help_des="Admin command to close the mcf minecraft tournament form.", required_roles=["nova_admin"], also_run_parent_CMD=False)
        async def close_form(self:MCF, ctx:GoldyBot.objects.slash.InteractionToCtx):
            tournament_info = _info_.TournamentInfo()

            avaliable_mcf_tournaments = []
            for tournament in await tournament_info.get_all_mcfs():
                if await tournament.is_form_open():
                    avaliable_mcf_tournaments.append(tournament)

            view = _forms_.MCFCloseFormDropdownView(GoldyBot.Member(ctx), avaliable_mcf_tournaments)

            await send(ctx, embed=GoldyBot.utility.goldy.embed.Embed(
                title="🛑 Which MCF?",
                description="**⏱ Pick the mcf you would like to close the form of.**",
                colour=GoldyBot.utility.goldy.colours.WHITE
            ), view=view)

        @mcf.sub_command(help_des="Admin command for generating teams.json file with every single player that signup.", required_roles=["nova_admin"], also_run_parent_CMD=False)
        async def teams_json_all(self:MCF, ctx:GoldyBot.objects.slash.InteractionToCtx):
            tournament_info = _info_.TournamentInfo()

            mcf = await tournament_info.get_latest_mcf()
            if not mcf == None:
                player_list = []

                for player_doc in await mcf.tournament_database.find_all(user_output.make_date_human(mcf.date)):
                    if not player_doc["_id"] == 0:
                        player_list.append({"uuid":player_doc["mc_uuid"], "username":player_doc["mc_ign"], "team_number":player_doc["team"], "discord_id":player_doc["_id"]})

                json_file = GoldyBot.files.File(__path__[0] + f"/teams_json_dump/mcf_teams_{user_output.make_date_human(mcf.date, date_format='%d_%m_%Y')}.json")
                json_file.create()

                json_file.write(json.dumps(player_list))
                
                await send(ctx, file=GoldyBot.nextcord.File(json_file.file_path))

            else:
                await send(ctx, embed=GoldyBot.utility.goldy.embed.Embed(
                    title="⛔ No MCF!",
                    description="**🛑 There's no mcf being hosted to generate a teams.json!**",
                    colour=GoldyBot.utility.goldy.colours.AKI_RED
                ))

        @mcf.sub_command(help_des="Admin command for generating randomized teams.json file.", required_roles=["nova_admin"], also_run_parent_CMD=False)
        async def teams_json_random(self:MCF, ctx:GoldyBot.objects.slash.InteractionToCtx):
            tournament_info = _info_.TournamentInfo()

            mcf = await tournament_info.get_latest_mcf()
            if not mcf == None:
                team_player_list:List[Dict[str, List[Dict[str, any]]]] = []
                actual_player_list:List[dict] = []

                max_team_count = int(mcf.max_players / 2)

                all_players_docs = await mcf.tournament_database.find_all(user_output.make_date_human(mcf.date))
                all_players_docs = all_players_docs[1:]
                random_.shuffle(all_players_docs)
                
                print(all_players_docs)

                # Catagrize players into teams
                for player_doc in all_players_docs:
                    player_team = player_doc["team"]

                    if not player_team == None:
                        teammate_player_doc = None

                        # Find teammate.
                        for random_player_doc in all_players_docs:
                            if not random_player_doc["_id"] == player_doc["_id"]:
                                if random_player_doc["team"] == player_team:
                                    teammate_player_doc = random_player_doc
                        
                        # Create team dict.
                        team_dict = {
                            f"{player_team}" : [
                                {"uuid":player_doc["mc_uuid"], "username":player_doc["mc_ign"], "team_number":player_team, "discord_id":player_doc["_id"]},
                                {"uuid":teammate_player_doc["mc_uuid"], "username":teammate_player_doc["mc_ign"], "team_number":player_team, "discord_id":teammate_player_doc["_id"]}
                            ]
                        }
                        
                        # Add team dict to player list.
                        if not team_dict in team_player_list:
                            print("it's the same, bruh")
                            team_player_list.append(team_dict)

                    else:
                        teammate_player_doc = None

                        # Find a teammate that has no team.
                        for random_player_doc in all_players_docs:
                            if not random_player_doc["_id"] == player_doc["_id"]:
                                if random_player_doc["team"] == player_team:
                                    teammate_player_doc = random_player_doc
                        
                        # Create team dict.
                        team_dict = {
                            "team_number": f"{player_team}",

                            "players" : [
                                {"uuid":player_doc["mc_uuid"], "username":player_doc["mc_ign"], "team_number":player_team, "discord_id":player_doc["_id"]},
                                {"uuid":teammate_player_doc["mc_uuid"], "username":teammate_player_doc["mc_ign"], "team_number":player_team, "discord_id":teammate_player_doc["_id"]}
                            ]
                        }
                        
                        # Add team dict to player list.
                        if not team_dict in team_player_list:
                            print("it's the same, bruh")
                            team_player_list.append(team_dict)

                # Randomize again.
                random_.shuffle(team_player_list)
                
                # Limit to max teams allowed to play.
                team_player_list = team_player_list[:max_team_count]

                # Convert to teams.json list format.
                for team in team_player_list:
                    for player in team["players"]:
                        actual_player_list.append(player)

                json_file = GoldyBot.files.File(__path__[0] + f"/teams_json_dump/mcf_teams_{user_output.make_date_human(mcf.date, date_format='%d_%m_%Y')}.json")
                json_file.create()

                json_file.write(json.dumps(actual_player_list))
                
                await send(ctx, file=GoldyBot.nextcord.File(json_file.file_path))

            else:
                await send(ctx, embed=GoldyBot.utility.goldy.embed.Embed(
                    title="⛔ No MCF!",
                    description="**🛑 There's no mcf being hosted to generate a teams.json!**",
                    colour=GoldyBot.utility.goldy.colours.AKI_RED
                ))

        @mcf.sub_command(help_des="Admin command for canceling an MCF tournament.", required_roles=["nova_admin"], also_run_parent_CMD=False)
        async def cancel(self:MCF, ctx:GoldyBot.objects.slash.InteractionToCtx):
            tournament_info = _info_.TournamentInfo()
            
            view = _forms_.MCFCancelDropdownView(GoldyBot.Member(ctx), await tournament_info.get_all_mcfs())

            await send(ctx, embed=GoldyBot.utility.goldy.embed.Embed(
                title="🛑 Which MCF?",
                description="**⏱ Pick the mcf you would like to cancel.**",
                colour=GoldyBot.utility.goldy.colours.WHITE
            ), view=view)