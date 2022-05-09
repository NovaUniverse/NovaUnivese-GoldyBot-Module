import GoldyBot
import datetime
import dateparser

database:GoldyBot.Database = GoldyBot.cache.main_cache_dict["database"]
mcf_database = database.new_instance("mcf_data")

class JoinMCFForm(GoldyBot.nextcord.ui.Modal):
    def __init__(self, teammate:GoldyBot.nextcord.Member=None):
        super().__init__(
            "Join 🔥 MCF Tournament",
        )

        self.teammate = teammate

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
        if not self.teammate == None:
            await interaction.send(f'**✉️ Team Up Inventation Sent to ``fdjfhudhfydu REEEEH!!!``! ✅**')

class OpenMCFForm(GoldyBot.nextcord.ui.Modal):
    def __init__(self):
        super().__init__(
            "🔓 Open 🔥 MCF Tournament",
        )

        self.tournament_date = GoldyBot.nextcord.ui.TextInput(
            label="Tournament Date",
            style=GoldyBot.nextcord.TextInputStyle.short,
            placeholder="The damn date you idiot!",
            default_value=f"{datetime.date.today().strftime('%d/%m/%Y')}",
            required=True,
            min_length=5,
        )
        self.add_item(self.tournament_date)

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
        if self.tournament_date.value in await mcf_database.list_collection_names():
            await interaction.send(f"**🔥 There's already been an mcf for that date. *Dev Goldy was lazy 😴 while coding this so your going to have to remove this mcf from the mcf_database manually. 😀* ❌**")
            #TODO: Replace these disgusting messages with embeds.
            return

        else:
            await mcf_database.create_collection(self.tournament_date.value, {"_id": 0, 
            "date": dateparser.parse(self.tournament_date.value, date_formats=["%d/%m/%Y", "%Y/%m/%d"]).timestamp(),
            "max_players": int(self.max_players.value)
            })

            await interaction.send(f'**🔥 MCF Form is now open. ``/join_mcf`` ✅**')