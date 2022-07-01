from typing import Dict, List
import GoldyBot
import datetime
import dateparser

from GoldyBot.utility.datetime import user_output

from . import _tournament_, _player_, _info_

database:GoldyBot.Database = GoldyBot.cache.main_cache_dict["database"]
mcf_database = database.new_instance("mcf_data")

class JoinMCFForm(GoldyBot.nextcord.ui.Modal):
    def __init__(self, tournament:_tournament_.MCFTournament):
        super().__init__(
            "Join 🔥 MCF Tournament",
        )

        self.tournament = tournament

        self.time_agree = GoldyBot.nextcord.ui.TextInput(
            label="Will you be on time? (Saturday 18:00 GMT+1)",
            style=GoldyBot.nextcord.TextInputStyle.short,
            placeholder="Yes",
            default_value="No",
            required=True,
            min_length=2,
            max_length=3
        )
        self.add_item(self.time_agree)

        self.mc_username = GoldyBot.nextcord.ui.TextInput(
            label="Enter Minecraft IGN",
            placeholder="Minecraft IGN...",
            required=True
        )
        self.add_item(self.mc_username)

    async def callback(self, interaction: GoldyBot.nextcord.Interaction) -> None:
        mcf_player = _player_.MCFPlayer(interaction, 
            self.mc_username.value)

        await self.tournament.add_player(mcf_player)

        embed = GoldyBot.utility.goldy.embed.Embed(
            title="✅ Join Request Sent!",
            colour=GoldyBot.utility.goldy.colours.GREEN,
            description=f"""
            **Your form has been sent. You've been added to the tournament player list. As the tournament date approaches, you'll be pinged in <#7188671160430632> when your in!**

            **[How to Team with Friends?]()**
            """)

        # Move this message to a discord server help channel.
        """💌 To team with a friend they must also do ``/join_mcf`` and then your able to send each other team requests via ``/mcf_team``. 😊"""

        await interaction.send(embed=embed)

class OpenMCFForm(GoldyBot.nextcord.ui.Modal):
    def __init__(self):
        super().__init__(
            "🔓 Open 🔥 MCF Tournament",
        )

        self.tournament_date = GoldyBot.nextcord.ui.TextInput(
            label="Tournament Date",
            style=GoldyBot.nextcord.TextInputStyle.short,
            placeholder="The damn date you idiot! Like --> 13/05/2022",
            default_value=f"{datetime.date.today().strftime('%d/%m/%Y')}",
            required=True,
            min_length=6,
        )
        self.add_item(self.tournament_date)

        self.tournament_time = GoldyBot.nextcord.ui.TextInput(
            label="Tournament Time",
            style=GoldyBot.nextcord.TextInputStyle.short,
            placeholder="The damn time you idiot! Like --> 18:00",
            default_value=f"{datetime.datetime.now().strftime('%H:%M')}",
            required=True,
            min_length=5,
        )
        self.add_item(self.tournament_time)

        # Settings
        self.max_players = GoldyBot.nextcord.ui.TextInput(
            style=GoldyBot.nextcord.TextInputStyle.short,
            label="Max Players",
            placeholder="Max players, UwU!",
            default_value="24",
            required=True
        )
        self.add_item(self.max_players)

    async def callback(self, interaction: GoldyBot.nextcord.Interaction) -> None:
        
        # Create the tournament.
        #==========================
        mcf = _tournament_.MCFTournament(mcf_database, self.tournament_date.value, self.tournament_time.value, self.max_players.value)

        await mcf.init()

        if mcf.was_created:
            embed = GoldyBot.utility.goldy.embed.Embed(
                title="🔥 MCF Form now open!",
                description=f"""
                **✅ MCF Form is now open until ``{user_output.make_time_human(mcf.date)} ({datetime.datetime.now().astimezone().tzinfo})`` on ``{user_output.make_date_human(mcf.date)}`` ✅**

                ``/join_mcf``
                """,
                colour=GoldyBot.utility.goldy.colours.AKI_ORANGE)

            await interaction.send(embed=embed)
        
        else:
            embed = GoldyBot.utility.goldy.embed.Embed(
                title="❌ MCF already exists!",
                description=f"""
                **🔥 There's already an mcf for that date.** ❌

                **``/mcf_cancel`` to cancel it.**
                """)

            await interaction.send(embed=embed)

class MCFCancelDropdown(GoldyBot.nextcord.ui.Select):
    def __init__(self, author:GoldyBot.Member, mcf_tournaments:List[_tournament_.MCFTournament]):
        self.author = author

        count = 0

        options = []
        self.options_values = {}

        for tournament in mcf_tournaments:
            count += 1
            options.append(GoldyBot.nextcord.SelectOption(
                label=f"• MCF - {user_output.make_date_human(tournament.date)}", 
                description=f"Time: {user_output.make_time_human(tournament.date)}", 
                emoji="🏆",
                value=count))

            self.options_values[f"{count}"] = tournament

        super().__init__(
            placeholder="🎯 Choose the tournament to cancel.",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: GoldyBot.nextcord.Interaction):
        view = MCFCancelConfirm(self.author)
        await interaction.send("**Are you sure you would like to cancel this Tournament?**", view=view)
        await view.wait()

        if view.value == True:
            mcf:_tournament_.MCFTournament = self.options_values[self.values[0]]

            if await mcf.delete():
                embed = GoldyBot.utility.goldy.embed.Embed(
                    title="⛔ MCF Cancelled!",
                    description=f"""
                    **❌ The MCF for ``{user_output.make_date_human(mcf.date)}`` has been cancelled!** 
                    """,
                    colour=GoldyBot.utility.goldy.colours.AKI_RED)

                await interaction.send(embed=embed)

class MCFCancelDropdownView(GoldyBot.nextcord.ui.View):
    def __init__(self, author:GoldyBot.Member, mcf_tournaments:List[_tournament_.MCFTournament]):
        super().__init__()

        self.add_item(MCFCancelDropdown(author, mcf_tournaments))

class MCFCancelConfirm(GoldyBot.nextcord.ui.View):
    def __init__(self, author:GoldyBot.Member):
        super().__init__()
        self.value = None

        self.author = author

    @GoldyBot.nextcord.ui.button(label="Yes", style=GoldyBot.nextcord.ButtonStyle.green)
    async def yes(self, button: GoldyBot.nextcord.ui.Button, interaction: GoldyBot.nextcord.Interaction):
        if self.author.member == interaction.user:
            await interaction.response.send_message("**Okay! 💛**", ephemeral=True)
            self.value = True
            self.stop()

    @GoldyBot.nextcord.ui.button(label="NO!", style=GoldyBot.nextcord.ButtonStyle.red)
    async def no(self, button: GoldyBot.nextcord.ui.Button, interaction: GoldyBot.nextcord.Interaction):
        if self.author.member == interaction.user:
            await interaction.response.send_message("**Alright, cancelled! 💚**", ephemeral=True)
            self.value = False
            self.stop()