import discord
from discord import app_commands
from discord.ext import commands
from db.config_manager import get_guild_config, update_guild_config, reset_guild_config
from googletrans import LANGUAGES, LANGCODES

# All customize commands here have an option value parameter
# If no value is given, instead send an embed for what the command does

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        # Make config the parent command, with every other command in here being a subcommand
        # A user must have admin perms to use any commands here
        self.config = app_commands.Group(
                                    name="config",
                                    description="All configuration commands",
                                    default_permissions=discord.Permissions(administrator=True)
                                    )
        # Init all commands as children on config
        self.config.command(name="view", description="View the server's LangBot configurations")(self.view)
        self.config.command(name="reset", description="Reset all configurations to their default values")(self.reset)
        self.config.command(name="translation-reply-message", description="Leave value parameter blank to get more info")(self.translation_reply_message)
        self.config.command(name="target-language", description="Leave value parameter blank to get more info")(self.target_lang)
        self.config.command(name="ignore-languages", description="Leave value parameter blank to get more info")(self.ignore_langs)
        self.config.command(name="ignore-bots", description="Leave value parameter blank to get more info")(self.ignore_bots)
        # ...
        # Add this parent command to the command tree
        self.bot.tree.add_command(self.config)
    
    async def view(self, interaction: discord.Interaction):
        """View all configurations as an embed"""
        await interaction.response.defer(ephemeral=True)
        # Get the guilds config
        db_config = await get_guild_config(interaction.guild_id)
        
        # Description of the embed
        description = """**Translation Reply Message**
        • Message format when the bot replies with a translation.
        **Target Language**
        • The language the bot should translate to.
        **Ignore Languages**
        • The languages to ignore when someone sends a message.
        **Ignore Bots**
        • Should the bot ignore other bots messages, regardless of the language their message was sent in."""
        
        # The actual embed
        embed = discord.Embed(
            title="LangBot Configuration",
            description=description,
            color=discord.Color.blue()
        )
        
        # For every item in "ignore languages", convert the code (such as "en") to the name (such as "English")
        code_to_name = [LANGUAGES.get(ignore_lang, "").capitalize() for ignore_lang in db_config["IGNORE_LANGS"]]
        
        # Add all config options as fields in the embed
        embed.add_field(name="Translation Reply Message", value=f"`{db_config['TRANSLATE_REPLY_MESSAGE']}`", inline=False)
        embed.add_field(name="Target Language", value=LANGUAGES[db_config["TARGET_LANG"]].capitalize(), inline=False)
        embed.add_field(name="Ignore Languages", value=", ".join(code_to_name), inline=False)
        embed.add_field(name="Ignore Bots", value=db_config["IGNORE_BOTS"], inline=False)
        
        await interaction.followup.send(embed=embed, ephemeral=True)
        print(f"{interaction.user.display_name} used the config/view command in {interaction.channel.name}/{interaction.guild.name}")
    
    async def reset(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        await reset_guild_config(interaction.guild_id)
        await interaction.followup.send("I have reset all LangBot configurations for this guild!", ephemeral=True)
        print(f"{interaction.user.display_name} used the config/reset command in {interaction.channel.name}/{interaction.guild.name}")
    
    async def translation_reply_message(
        self, interaction: discord.Interaction,
        value: str = None
    ):
        await interaction.response.defer(ephemeral=True)
        
        if value is None:
            # Get the guilds config
            config = await get_guild_config(interaction.guild_id)
            description = f"""Current value: `{config["TRANSLATE_REPLY_MESSAGE"]}`
            This message will be sent when a user sends a message in another language.
            Placeholders are defined below."""
            
            # The embed alongside fields to send to the user
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
            # Update the config with the desired value
            await update_guild_config(interaction.guild_id, "TRANSLATE_REPLY_MESSAGE", value)
            await interaction.followup.send(f'Successfully updated "Translate Reply Message" to `{value}`', ephemeral=True)
            print(f"{interaction.user.display_name} used the config/translation-reply-message command in {interaction.channel.name}/{interaction.guild.name}")
    
    async def target_lang(
        self, interaction: discord.Interaction,
        value: str = None
    ):
        await interaction.response.defer(ephemeral=True)
        
        if value is None:
            # Get the guilds config
            config = await get_guild_config(interaction.guild_id)
            description = f"""Current value: `{LANGUAGES[config["TARGET_LANG"]].capitalize()}`
            The language that untranslated text should be translated into.
            Can either be a language code (such as `en`), or language name (such as `english`).
            Use the `/support` command to view all supported languages."""
            
            # The embed to reply with
            embed = discord.Embed(
                title="Target Language",
                description=description,
                color=discord.Color.blue()
            )
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            print(f"{interaction.user.display_name} used the config/target-lang command in {interaction.channel.name}/{interaction.guild.name}")
        else:
            # Clean the value, making it lowercase and stripped
            value = value.lower().strip()
            # If the value is not a valid language code (such as "en")
            if value not in LANGUAGES.keys():
                # If the value is not a valid language name (such as "england")
                if value not in LANGCODES.keys():
                    return await interaction.followup.send(f"`{value}` is an invalid language, use the `/supported` command to view all valid languages")
                else:
                    # If the value is a valid country name, convert it into its key code
                    value = LANGCODES.get(value)
            await update_guild_config(interaction.guild_id, "TARGET_LANG", value)
            await interaction.followup.send(f'Successfully updated "Target Language" to `{LANGUAGES[value].capitalize()}`', ephemeral=True)

    async def ignore_langs(
        self, interaction: discord.Interaction,
        value: str = None
    ):
        await interaction.response.defer(ephemeral=True)
        
        if value is None:
            # Get the guilds config
            config = await get_guild_config(interaction.guild_id)
            description = f"""Current value: `{", ".join(LANGUAGES[i].capitalize() for i in config["IGNORE_LANGS"])}`
            The language(s) that the bot should ignore.
            Separate languages with commas (,).
            Can either be a language code (such as `en`), or language name (such as `english`).
            Example: `en, pl, fr`
            Another example: `english, french, polish`"""
            
            # The embed to reply with
            embed = discord.Embed(
                title="Ignore Languages",
                description=description,
                color=discord.Color.blue()
            )
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            print(f"{interaction.user.display_name} used the config/ignore-langs command in {interaction.channel.name}/{interaction.guild.name}")
        else:
            # Clean the value, making it lower case, stripped, and replace all spaces with empty characters (remove spaces)
            value = value.strip().lower().replace(" ", "")
            
            # If there is at least one comma in the input
            if "," in value:
                # Split the input with each comma, creating a list
                value = value.split(",")
                
                # Loop through this newly created list to ensure it is valid
                for i, item in enumerate(value):
                    # If it is not a valid language code (such as "en")
                    if item not in LANGUAGES.keys():
                        # If it is not a valid language name (such as "england")
                        if item not in LANGCODES.keys():
                            return await interaction.followup.send(f"`{value}` is not a valid language code or name, use `/supported` to view valid languages", ephemeral=True)
                        else:
                            # Convert the language name, into the language code
                            value[i] = LANGCODES.get(item)
            # There is no comma, meaning there is only one item
            else:
                # If the item is not a valid language code
                if value not in LANGUAGES.keys():
                    # If the item is not a valid language name
                    if value not in LANGCODES.keys():
                        return await interaction.followup.send(f"`{value}` is not a valid language code or name, use `/supported` to view valid languages", ephemeral=True)
                    else:
                        # Convert the language name into a language code, and convert it into a list
                        value = list(LANGCODES.get(value))
            await update_guild_config(interaction.guild_id, "IGNORE_LANGS", value)
            await interaction.followup.send(f'Successfully updated "Ignore Languages" to `{", ".join([LANGUAGES[i].capitalize() for i in value])}`', ephemeral=True)
    
    async def ignore_bots(
        self, interaction: discord.Interaction,
        value: bool = None
    ):
        await interaction.response.defer(ephemeral=True)
        
        if value is None:
            # Get the config of the guild
            config = await get_guild_config(interaction.guild_id)
            description = f"""Current value: `{config["IGNORE_BOTS"]}`
            Should the bot ignore other bots, regardless of the language they send."""
            
            # The embed to reply with
            embed = discord.Embed(
                title="Ignore Bots",
                description=description,
                color=discord.Color.blue()
            )
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            
        else:
            await update_guild_config(interaction.guild_id, "IGNORE_BOTS", value)
            await interaction.followup.send(f'Successfully updated "Ignore Bots" to `{value}`', ephemeral=True)
            print(f"{interaction.user.display_name} used the config/ignore-bots command in {interaction.channel.name}/{interaction.guild.name}")

# Setup the commands
async def setup(bot):
    # Add the commands cog
    await bot.add_cog(Config(bot))