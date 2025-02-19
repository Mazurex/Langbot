import discord
from discord.ext import commands
from googletrans import LANGUAGES, LANGCODES, Translator
import math

translator = Translator()

class LanguagePaginator(discord.ui.View):
    def __init__(self, user: discord.Member, languages, chunk_size=25):
        super().__init__()
        self.user = user
        self.languages = languages
        self.chunk_size = chunk_size
        self.current_page = 0
        self.total_pages = math.ceil(len(languages) / chunk_size)
        
        self.update_buttons()
    
    def update_buttons(self):
        """Disables buttons when on the first or last page"""
        self.previous_page.disabled = self.current_page == 0
        self.next_page.disabled = self.current_page == self.total_pages - 1
    
    def format_page(self):
        """Formats the embed for the current page"""
        start = self.current_page * self.chunk_size
        end = start + self.chunk_size
        page_languages = list(self.languages.items())[start:end]
        
        description = "\n".join([f"**{code.upper()}** - {name}" for code, name in page_languages])
        embed = discord.Embed(
            title=f"🌍 Supported Languages (Page {self.current_page + 1}/{self.total_pages})",
            description=description,
            color=discord.Color.blue()
        )
        return embed
    
    async def update_message(self, interaction: discord.Interaction):
        """Updates the embed when a button is clicked"""
        self.update_buttons()
        embed = self.format_page()
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Ensures only the command author can use the buttons"""
        return interaction.user == self.user
        
    @discord.ui.button(label="<", style=discord.ButtonStyle.blurple)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Go to the previous page"""
        if self.current_page > 0:
            self.current_page -= 1
            await self.update_message(interaction)
            
    @discord.ui.button(label=">", style=discord.ButtonStyle.blurple)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Go to the next page"""
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            await self.update_message(interaction)

class TranslateCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @discord.app_commands.command(name="translate", description="Translate any text into any desired language")
    @discord.app_commands.describe(text="The text to translate")
    @discord.app_commands.describe(target="The target language to translate to, run /supported to view valid languages. Defaults to 'en'")
    async def translate(
        self, interaction: discord.Interaction,
        text: str,
        target: str = "en"
    ):
        if target.lower() not in LANGUAGES.keys():
            if target in LANGCODES.keys():
                target = LANGCODES.get(target)
            else:
                return await interaction.response.send_message(f"`{target}` is not a valid country code/name, run `/supported` to view all valid country codes", ephemeral=True)
        
        try:
            translated = await translator.translate(text, dest=target)
            lang_from = await translator.detect(text)
            
            response = f"**[{LANGUAGES[lang_from.lang].capitalize()} ➜ {LANGUAGES[target].capitalize()}]**\n{translated.text}"
            await interaction.response.send_message(response, ephemeral=True)
            print(f"{interaction.user.display_name} used the translate command in {interaction.channel.name}/{interaction.guild.name}")
        except Exception as e:
            await interaction.response.send_message("There was an error with this command!", ephemeral=True)
            print(f"Error with translate command: {e}")
    
    @discord.app_commands.command(name="supported", description="View a paginated embed of all supported languages")
    async def supported(
        self, interaction: discord.Interaction
    ):
        await interaction.response.defer(ephemeral=True)
        
        view = LanguagePaginator(user=interaction.user, languages=LANGUAGES)
        embed = view.format_page()
        
        await interaction.followup.send(embed=embed, view=view, ephemeral=True)
        print(f"{interaction.user.display_name} used the supported command in {interaction.channel.name}/{interaction.guild.name}")

async def setup(bot):
    await bot.add_cog(TranslateCmds(bot))