import discord
from discord.ext import commands
from utils.utils import valid_code, internal_print_log_message
from i_logger.logger import log
import math

# Custom made translation API
from TranslationAPI.translate import translate
from TranslationAPI.constants import LANGUAGES

from db.config_manager import get_guild_config, get_channel_config

class LanguagePaginator(discord.ui.View):
    """As there are over 300 languages, making one embed is not smart
    So we create a paginated embed, allowing the user to cycle through pages"""
    def __init__(self, user: discord.Member, languages, chunk_size=25):
        super().__init__()
        self.user = user
        self.languages = languages
        self.chunk_size = chunk_size
        self.current_page = 0
        self.total_pages = math.ceil(len(languages) / chunk_size)
    
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
        else:
            # If user is on the first page, go to the last page
            self.current_page = self.total_pages - 1
        await self.update_message(interaction)
            
    @discord.ui.button(label=">", style=discord.ButtonStyle.blurple)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Go to the next page"""
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
        else:
            # If user is on the last page, go to the first page
            self.current_page = 0
        await self.update_message(interaction)

class TranslateCmds(commands.Cog):
    """All commands related to translating"""
    def __init__(self, bot):
        self.bot = bot
    
    # Create info about the command and its parameters
    @discord.app_commands.command(name="translate", description="Translate any text into any desired language")
    @discord.app_commands.describe(text="The text to translate")
    @discord.app_commands.describe(target="The target language to translate to, run /supported to view valid languages. Defaults to the guilds target language")
    async def translate(
        self, interaction: discord.Interaction,
        text: str,
        target: str = None
    ):
        config = await get_guild_config(interaction.guild_id)
        channel_config = await get_channel_config(interaction.guild_id, interaction.channel_id)
        # If the user doesn't specify a language, set it to the target language in the guild's channel/global config
        if target is None:
            target = channel_config["TARGET_LANG"]
        
        is_valid, target = valid_code(target.lower())

        if not is_valid:
            return await interaction.response.send_message(f"`{target}` is not a valid country code/name, run `/supported` to view all valid country codes", ephemeral=True)

        try:
            # Translate the text into the target language, as well as detect what language the original message was in
            translated, lang_from = translate(text, target_lang=target)
            
            # Create the response for the message, showing what language its translating from and to
            response = f"**[{LANGUAGES[lang_from].capitalize()} ➜ {LANGUAGES[target].capitalize()}]**\n{translated}"
            await interaction.response.send_message(response, ephemeral=True)
            internal_print_log_message(interaction, "translate")
        except Exception as e:
            await interaction.response.send_message("There was an error with this command!", ephemeral=True)
            log(f"Error with translate command: {e}", "critical")
    
    # Create info about the command
    @discord.app_commands.command(name="supported", description="View a paginated embed of all supported languages")
    async def supported(
        self, interaction: discord.Interaction
    ):
        await interaction.response.defer(ephemeral=True)
        
        # Create an instance of the paginator
        view = LanguagePaginator(user=interaction.user, languages=LANGUAGES)
        # Embed for each page
        embed = view.format_page()
        
        await interaction.followup.send(embed=embed, view=view, ephemeral=True)
        internal_print_log_message(interaction, "supported")

# Setup the commands
async def setup(bot):
    # Add the commands to the cog
    await bot.add_cog(TranslateCmds(bot))