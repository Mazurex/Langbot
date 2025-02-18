import discord
from discord import app_commands
from discord.ext import commands
from db.config_manager import get_guild_config, update_guild_config, reset_guild_config
from googletrans import LANGUAGES, LANGCODES

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        self.config = app_commands.Group(
                                    name="config",
                                    description="All configuration commands",
                                    default_permissions=discord.Permissions(administrator=True)
                                    )
        self.config.command(name="view", description="View the server's LangBot configurations")(self.view)
        self.config.command(name="reset", description="Reset all configurations to their default values")(self.reset)
        self.config.command(name="translation-reply-message", description="Leave value parameter blank to get more info")(self.translation_reply_message)
        self.config.command(name="target-language", description="Leave value parameter blank to get more info")(self.target_lang)
        # ...
        self.bot.tree.add_command(self.config)
    
    async def view(self, interaction: discord.Interaction):
        """View all config options as an embed"""
        await interaction.response.defer(ephemeral=True)
        db_config = await get_guild_config(interaction.guild_id)
        
        description = """**Translation Reply Message**
        • Message format when the bot replies with a translation.
        **Target Language**
        • The language the bot should translate to.
        **Ignore Languages**
        • The languages to ignore when someone sends a message.
        **Ignore Bots**
        • Should the bot ignore other bots messages, regardless of the language their message was sent in."""
        
        embed = discord.Embed(
            title="LangBot Configuration",
            description=description,
            color=discord.Color.blue()
        )
        
        code_to_name = [LANGUAGES.get(ignore_lang, "").capitalize() for ignore_lang in db_config["IGNORE_LANGS"]]
        
        embed.add_field(name="Translation Reply Message", value=f"`{db_config['TRANSLATE_REPLY_MESSAGE']}`", inline=False)
        embed.add_field(name="Target Language", value=LANGUAGES[db_config["TARGET_LANG"]].capitalize(), inline=False)
        embed.add_field(name="Ignore Languages", value=", ".join(code_to_name), inline=False)
        embed.add_field(name="Ignore Bots", value=db_config["IGNORE_BOTS"], inline=False)
        
        await interaction.followup.send(embed=embed, ephemeral=True)
    
    async def reset(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        await reset_guild_config(interaction.guild_id)
        await interaction.followup.send("I have reset all LangBot configurations for this guild!", ephemeral=True)
    
    async def translation_reply_message(
        self, interaction: discord.Interaction,
        value: str = None
    ):
        await interaction.response.defer(ephemeral=True)
        
        if value is None:
            config = await get_guild_config(interaction.guild_id)
            description = f"""Current value: `{config["TRANSLATE_REPLY_MESSAGE"]}`
            This message will be sent when a user sends a message in another language.
            Placeholders are defined below."""
            
            embed = discord.Embed(
                title="Translate Reply Message",
                description=description,
                color=discord.Color.blue()
            )
            embed.add_field(name="`{flag}`", value="The flag of the untranslated languages country", inline=False)
            embed.add_field(name="`{translated}`", value="The translated message", inline=False)
            embed.add_field(name="`{original}`", value="The original untranslated message", inline=False)
            embed.add_field(name="`{author_id}`", value="The ID of the author of the message", inline=False)
            embed.add_field(name="`{guild_id}`", value="The ID of the guild of the message", inline=False)
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            
        else:
            await update_guild_config(interaction.guild_id, "TRANSLATE_REPLY_MESSAGE", value)
            await interaction.followup.send(f'Successfully updated "Translate Reply Message" to `{value}`', ephemeral=True)
    
    async def target_lang(
        self, interaction: discord.Interaction,
        value: str = None
    ):
        await interaction.response.defer(ephemeral=True)
        
        if value is None:
            config = await get_guild_config(interaction.guild_id)
            description = f"""Current value: `{LANGUAGES[config["TARGET_LANG"]].capitalize()}`
            The language that untranslated text should be translated into.
            Can either be a language code (such as `en`), or language name (such as `english`)."""
            
            embed = discord.Embed(
                title="Target Language",
                description=description,
                color=discord.Color.blue()
            )
            
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            value = value.lower().strip()
            if value not in LANGUAGES.keys():
                if value in LANGCODES.keys():
                    value = LANGCODES.get(value)
                else:
                    return await interaction.followup.send(f"`{value}` is an invalid language, use the `/supported` command to view all valid languages")
            await update_guild_config(interaction.guild_id, "TARGET_LANG", value)
            await interaction.followup.send(f'Successfully updated "Target Language" to `{LANGUAGES[value].capitalize()}`', ephemeral=True)

    async def ignore_langs(
        self, interaction: discord.Interaction,
        value: str = None
    ):
        pass
    
    async def ignore_bots(
        self, interaction: discord.Interaction,
        value: bool = None
    ):
        pass

async def setup(bot):
    await bot.add_cog(Config(bot))