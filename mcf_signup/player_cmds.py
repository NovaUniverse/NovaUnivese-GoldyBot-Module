import asyncio
from datetime import datetime
from typing import List
import GoldyBot
from GoldyBot.utility.commands import *

from . import objects
from . import database
from . import Background_Images, PATH

mcf_database = GoldyBot.cache.database().new_instance("mcf_data")

class MCFSignup(GoldyBot.Extension):
    def __init__(self, package_module=None):
        super().__init__(self, package_module_name=package_module)

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

        self.join_request_sent = GoldyBot.utility.goldy.embed.Embed(
            title="✅ 🏆 Join Request Sent!",
            colour=GoldyBot.Colours.AKI_ORANGE,
            description="""
***{} Your form has been processed.***

*You've been added to the tournament player list. As the tournament date approaches, you'll be pinged in <#7188671160430632> when your in!*

**💌 To team with a friend they must also register with {}, then you'll be able to team together with {}. 😊**
""")

        self.youve_been_removed_embed = GoldyBot.utility.goldy.embed.Embed(
            title="🧳 You've been removed!",
            description="""
            🚚 You've been removed from this mcf.
            """,
            colour=GoldyBot.Colours.DISCORD_EMBED_INVISIBLE
        )

        self.your_already_registered_embed = GoldyBot.utility.goldy.embed.Embed(
            title="💚 Your already in! 😊",
            description=f"""
            ✔ You're already registered for this upcoming mcf.
            """,
            colour=GoldyBot.Colours.DISCORD_EMBED_INVISIBLE,
        )
        self.your_already_registered_embed.footer.text = "(Notice: Just a reminder that this doesn't mean your actually confirmed to be playing.)"

        self.your_not_in_this_tournament_embed = GoldyBot.utility.goldy.embed.Embed(
            title="❤ Your not in this tournament!",
            description=f"""
            ⚠ You're not registered for this mcf.
            """,
            colour=GoldyBot.Colours.DISCORD_EMBED_INVISIBLE
        )

        self.agree_to_time = GoldyBot.utility.goldy.embed.Embed(
            title="❌ Agree to the time!",
            description=f"""
            ⚠ You MUST replace ``No`` with ``Yes`` to agree to the tournament time.
            """,
            colour=GoldyBot.Colours.RED
        )


    def loader(self):

        @GoldyBot.command(help_des="A command for players to sign up for the MCF tournament.", slash_cmd_only=True)
        async def mcf(self:MCFSignup, ctx):
            pass


        @mcf.sub_command()
        async def join(self:MCFSignup, ctx):
            tournament_data = await database.McfDataUtils(ctx, mcf_database).get_latest_tournament()
            tournament = database.Tournament(ctx, tournament_data)

            member = GoldyBot.Member(ctx)

            data = await tournament.get_tournament_data()
            player_in_tournament = await tournament.player_in_tournament(member, data)

            # Check if member is already in tournament.
            if not player_in_tournament:
                async def signup_player(answers:List[str], interaction):
                    ign = answers[0]
                    agree = answers[1]

                    if agree.lower() == "yes":
                        player_data = objects.PlayerData(member, ign, tournament.free_team(data), pending_teammate=None) #TODO: Replace team num with free team method.
                        
                        await tournament.add_player(player_data)

                        # Notify member.
                        embed = self.join_request_sent.copy()
                        embed.description = self.join_request_sent.description.format(mention(member), join.mention(), team.mention())
                        embed.set_image("attachment://image.png")

                        await send(ctx, embed=embed, file=GoldyBot.nextcord.File(GoldyBot.File(Background_Images().get_random()).file_path, filename="image.png"))

                    else:
                        # Notify member that they did not agree to the time.
                        embed = self.agree_to_time.copy()
                        embed.set_image("attachment://image.gif")
                        message = await send(interaction, embed=embed, file=GoldyBot.nextcord.File(GoldyBot.File(PATH + "/assets/agree_to_time.gif").file_path, filename="image.gif"))
                        await message.delete(delay=25)

                # Send Signup Form
                await send_modal(ctx, 
                    GoldyBot.utility.views.forms.normal_form(
                        title = "🏆 Play In 🔥MCF!",
                        items = [
                            GoldyBot.nextcord.ui.TextInput(
                                label="Minecraft IGN: ", style=GoldyBot.nextcord.TextInputStyle.short, placeholder="THEGOLDENPRO", required=True
                            ),
                            GoldyBot.nextcord.ui.TextInput(
                                label=f"Will you make it? ({tournament_data.time_and_date.strftime('%A, %d %b')})", 
                                style=GoldyBot.nextcord.TextInputStyle.short,
                                placeholder="Type 'Yes' to agree...",
                                default_value="No",
                                min_length=2,
                                max_length=3
                            )
                        ],
                        callback = signup_player,
                        author = GoldyBot.Member(ctx)
                    )
                )

            else:
                # Notify member they already are in.
                message = await send(ctx, embed=self.your_already_registered_embed)
                await message.delete(delay=6)


        @mcf.sub_command()
        async def leave(self:MCFSignup, ctx):
            tournament_data = await database.McfDataUtils(ctx, mcf_database).get_latest_tournament()
            tournament = database.Tournament(ctx, tournament_data)

            member = GoldyBot.Member(ctx)

            player_in_tournament = await tournament.player_in_tournament(member, await tournament.get_tournament_data())

            await think(ctx)

            if player_in_tournament:
                player_data = objects.PlayerData(member, None, None, None) # Your only need member object in player data to remove the player.
                
                await tournament.remove_player(player_data)

                # Notify player they have been removed.
                message = await send(ctx, embed=self.youve_been_removed_embed)
                await message.delete(delay=6)
            else:
                # Notify player their not in the tournament.
                message = await send(ctx, embed=self.your_not_in_this_tournament_embed)
                await message.delete(delay=6)


        @mcf.sub_command()
        async def team(self:MCFSignup, ctx):
            pass