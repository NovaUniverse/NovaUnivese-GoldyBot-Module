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

class CreateMCFForm(GoldyBot.nextcord.ui.Modal):
    def __init__(self):
        super().__init__(
            "🎁 Create 🔥 MCF Tournament",
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
                title="🔥 MCF has been created!",
                description=f"""
                **✅ MCF has been created for ``{user_output.make_time_human(mcf.date)} ({datetime.datetime.now().astimezone().tzinfo})`` on ``{user_output.make_date_human(mcf.date)}`` ✅**

                ``/mcf open_form`` - To open the form now.
                """,
                colour=GoldyBot.utility.goldy.colours.AKI_ORANGE)

            await interaction.send(embed=embed)
        
        else:
            embed = GoldyBot.utility.goldy.embed.Embed(
                title="❌ MCF already exists!",
                description=f"""
                **🔥 There's already an mcf for that date.** ❌

                **``/mcf cancel`` to cancel it.**
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
                description=f"⏰ {user_output.make_time_human(tournament.date)}", 
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
        view = await GoldyBot.utility.views.confirm.yes_or_no(interaction)
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


class MCFCloseFormDropdown(GoldyBot.nextcord.ui.Select):
    def __init__(self, author:GoldyBot.Member, mcf_tournaments:List[_tournament_.MCFTournament]):
        self.author = author

        count = 0

        options = []
        self.options_values = {}
        self.no_mcfs = False

        for tournament in mcf_tournaments:
            if tournament.is_open:
                count += 1
                options.append(GoldyBot.nextcord.SelectOption(
                    label=f"• MCF - {user_output.make_date_human(tournament.date)}", 
                    description=f"Time: {user_output.make_time_human(tournament.date)}", 
                    emoji="🏆",
                    value=count))

                self.options_values[f"{count}"] = tournament

        if options == []:
            options = [GoldyBot.nextcord.SelectOption(
                label=f"• There's no MCF being hosted!", 
                description=f"Time: 3am (UwU Time Zone)", 
                emoji="⛔",
                value="None")]

            self.no_mcfs = True

        super().__init__(
            placeholder="🎯 Choose the tournament to close form for.",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: GoldyBot.nextcord.Interaction):
        if self.no_mcfs == False:
            view = await GoldyBot.utility.views.confirm.yes_or_no(interaction)
            await interaction.send("**Are you sure you would like to close the form for this Tournament?**", view=view)
            await view.wait()

            if view.value == True:
                mcf:_tournament_.MCFTournament = self.options_values[self.values[0]]

                if not mcf == None:
                    if await mcf.close_form():
                        embed = GoldyBot.utility.goldy.embed.Embed(
                            title="🔒 MCF Form Closed!",
                            description=f"""
                            **❌ The form for the MCF hosting on ``{user_output.make_date_human(mcf.date)}`` has been closed!** 
                            """,
                            colour=GoldyBot.utility.goldy.colours.AKI_RED)

                        await interaction.send(embed=embed)

class MCFCloseFormDropdownView(GoldyBot.nextcord.ui.View):
    def __init__(self, author:GoldyBot.Member, mcf_tournaments:List[_tournament_.MCFTournament]):
        super().__init__()

        self.add_item(MCFCloseFormDropdown(author, mcf_tournaments))