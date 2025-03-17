import discord
from discord import app_commands
from discord.ext import commands
from db.config_manager import get_guild_config, update_guild_config, reset_guild_config
from utils.utils import LANGUAGES, f_translation_reply_message, f_target_lang, f_ignore_langs, f_ignore_bots, f_ignored_terms, f_reply, f_blacklisted_roles, f_auto_translate, internal_print_log_message
from i_logger.logger import log

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
        # Init all commands as children of config
        description = "Leave value parameter blank to get more info"
        self.config.command(name="view", description="View the server's LangBot configurations")(self.view)
        self.config.command(name="reset", description="Reset all configurations to their default values")(self.reset)
        self.config.command(name="translation-reply-message", description=description)(self.translation_reply_message)
        self.config.command(name="target-language", description=description)(self.target_lang)
        self.config.command(name="ignore-languages", description=description)(self.ignore_langs)
        self.config.command(name="ignore-bots", description=description)(self.ignore_bots)
        self.config.command(name="ignored-terms", description=description)(self.ignored_terms)
        self.config.command(name="reply", description=description)(self.reply)
        self.config.command(name="blacklisted-roles", description=description)(self.blacklisted_roles)
        self.config.command(name="auto-translate", description=description)(self.auto_translate)
        # ...
        # Add this parent command to the command tree
        self.bot.tree.add_command(self.config)
    
    async def view(self, interaction: discord.Interaction):
        """View all configurations as an embed"""
        await interaction.response.defer(ephemeral=True)
        # Get the guild config
        db_config = await get_guild_config(interaction.guild_id)
        
        # Description of the embed
        description = """config refers to guild-based config, or guild-default config.
        You can set a channel based config with `/channel-config`, more information in `/channel-config view`
        **Translation Reply Message**
        • Message format when the bot replies with a translation.
        **Target Language**
        • The language the bot should translate to.
        **Ignore Languages**
        • The languages to ignore when someone sends a message, just enter '\\*' to set it to nothing
        **Ignore Bots**
        • Should the bot ignore other bots messages, regardless of the language their message was sent in.
        **Ignored Terms**
        • If the untranslated, or translated message is equal to any of these terms, the translation will not be sent, just enter '\\*' to set it to nothing.
        **Reply**
        • Should the bot reply to the original untranslatd message.
        **Blacklisted Roles**
        • The bot will not translate any messages from users who have any blacklisted words, you can enter a mention, or a role ID, if you want to disable this feature, just enter '\\*' to set it to nothing.
        **Auto Translate**
        • If `true`, the bot will automatically translate messages that are not `ignored`"""
        
        # The actual embed
        embed = discord.Embed(
            title="LangBot Configuration",
            description=description,
            color=discord.Color.blue()
        )
        
        # For every item in "ignore languages", convert the code (such as "en") to the name (such as "English")
        ignore_languages = "None"
        if len(db_config["IGNORE_LANGS"]) > 0:
            ignore_languages = ", ".join([LANGUAGES.get(ignore_lang, "").capitalize() for ignore_lang in db_config["IGNORE_LANGS"]])
        
        ignored_terms = "None"
        if len(db_config["IGNORED_TERMS"]) > 0:
            ignore_languages = ", ".join(db_config["IGNORED_TERMS"])
        
        blacklisted_roles = "None"
        if len(db_config["BLACKLISTED_ROLES"]) > 0:
            blacklisted_roles = ", ".join(f"<@&{value}>" for value in db_config["BLACKLISTED_ROLES"])
        
        # Add all config options as fields in the embed
        embed.add_field(name="Translation Reply Message", value=f"`{db_config['TRANSLATE_REPLY_MESSAGE']}`", inline=False)
        embed.add_field(name="Target Language", value=LANGUAGES[db_config["TARGET_LANG"]].capitalize(), inline=False)
        embed.add_field(name="Ignore Languages", value=ignore_languages, inline=False)
        embed.add_field(name="Ignore Bots", value="Yes" if db_config["IGNORE_BOTS"] else "No", inline=False)
        embed.add_field(name="Ignored Terms", value=ignored_terms, inline=False)
        embed.add_field(name="Reply", value="Yes" if db_config["REPLY"] else "No", inline=False)
        embed.add_field(name="Blacklisted Roles", value=blacklisted_roles)
        embed.add_field(name="Auto Translate", value=db_config["AUTO_TRANSLATE"], inline=False)
        
        await interaction.followup.send(embed=embed, ephemeral=True)
        internal_print_log_message(interaction, "config/view")
    
    async def reset(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        await reset_guild_config(interaction.guild_id)
        await interaction.followup.send("I have reset all LangBot configurations for this guild!", ephemeral=True)
        internal_print_log_message(interaction, "config/reset")
    
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
            embed.add_field(name="`{lang_code}`", value="The language code of the untranslated message", inline=False)
            embed.add_field(name="`{lang_name}`", value="The language name of the untranslated message", inline=False)
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            
        else:
            # External function
            value = await f_translation_reply_message(value, interaction)
            await interaction.followup.send(f'Successfully updated "Translate Reply Message" to `{value}`', ephemeral=True)
    
    async def target_lang(
        self, interaction: discord.Interaction,
        value: str = None
    ):
        try:
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
                internal_print_log_message(interaction, "config/target-lang")
            else:
                # External function
                value = await f_target_lang(value, interaction)
                await interaction.followup.send(f'Successfully updated "Target Language" to `{LANGUAGES[value].capitalize()}`', ephemeral=True)
        except Exception as e:
            log(e, "critical")

    async def ignore_langs(
        self, interaction: discord.Interaction,
        value: str = None
    ):
        # Defer the reply
        await interaction.response.defer(ephemeral=True)
        config = await get_guild_config(interaction.guild_id)
        
        ignored_languages_str = "none"
        if len(config["IGNORE_LANGS"]) > 0:
            ignored_languages_str = ", ".join(LANGUAGES[i].capitalize() for i in config["IGNORE_LANGS"])
        
        if value is None:
            description = f"""Current value: `{ignored_languages_str}`
            The language(s) that the bot should ignore.
            Separate languages with commas (,).
            Can either be a language code (such as `en`), or language name (such as `english`).
            Example: `en, pl, fr`
            Another example: `english, french, polish`"""
            
            # An embed with information relating to the command
            embed = discord.Embed(
                title="Ignore Languages",
                description=description,
                color=discord.Color.blue()
            )
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            return

        # External function
        value = await f_ignore_langs(value, interaction)
        if not value:
            await interaction.followup.send('Successfuly disabled "Ignored Languages"')
        else:
        # Send a confirmation message
            await interaction.followup.send(f'Successfully updated "Ignored Languaes" to `{", ".join(value)}`', ephemeral=True)
    
    async def ignore_bots(
        self, interaction: discord.Interaction,
        value: bool = None
    ):
        await interaction.response.defer(ephemeral=True)
        
        if value is None:
            # Get the config of the guild
            config = await get_guild_config(interaction.guild_id)
            description = f"""Current value: `{"Yes" if config["IGNORE_BOTS"] else "No"}`
            Should the bot ignore other bots, regardless of the language they send."""
            
            # The embed to reply with
            embed = discord.Embed(
                title="Ignore Bots",
                description=description,
                color=discord.Color.blue()
            )
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            
        else:
            # External command
            value = await f_ignore_bots(value, interaction)
            await interaction.followup.send(f'Successfully updated "Ignore Bots" to `{"Yes" if value else "No"}`', ephemeral=True)

    async def ignored_terms(
        self, interaction: discord.Interaction,
        value: str = None
    ):
        await interaction.response.defer(ephemeral=True)
        config = await get_guild_config(interaction.guild_id)
        
        ignored_terms_str = "none"
        if len(config["IGNORED_TERMS"]) > 0:
            ignored_terms_str = ", ".join(config["IGNORED_TERMS"])
        
        if value is None:
            description = f"""Current value: `{ignored_terms_str}`
            If the translated/untranslated message contains any of these, don't send it
            Useful when there are terms that would be translated in other languages, such as 'lmaoo'.
            Separate values with commas (,).
            Example: `lmaoo, idk, test`"""
            # The embed to reply with
            embed = discord.Embed(
                title="Ignored Terms",
                description=description,
                color=discord.Color.blue()
            )
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            internal_print_log_message(interaction, "config/ignored-terms")
            
        else:
            value = await f_ignored_terms(value, interaction)

            if not value:
                await interaction.followup.send(f'Successfully disabled "Ignord Terms"', ephemeral=True)
            else:
                await interaction.followup.send(f'Successfully updated "Ignored Terms" to `{", ".join(value)}`', ephemeral=True)

    async def reply(
        self, interaction: discord.Interaction,
        value: bool = None
    ):
        await interaction.response.defer(ephemeral=True)
        
        if value is None:
            # Get the config of the guild
            config = await get_guild_config(interaction.guild_id)
            description = f"""Current value: `{"Yes" if config["REPLY"] else "No"}`
            Should the bot reply to the original untranslated message"""
            
            # The embed to reply with
            embed = discord.Embed(
                title="Reply",
                description=description,
                color=discord.Color.blue()
            )
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            
        else:
            # External command
            value = await f_reply(value, interaction)
            await interaction.followup.send(f'Successfully updated "Reply" to `{"Yes" if value else "No"}`', ephemeral=True)

    async def blacklisted_roles(
        self, interaction: discord.Interaction,
        value: str = None
    ):
        await interaction.response.defer(ephemeral=True)
        
        if value is None:
            # Get the config of the guild
            config = await get_guild_config(interaction.guild_id)
            description = f"""Current value: `{", ".join(map(str, config["BLACKLISTED_ROLES"])) if len(config["BLACKLISTED_ROLES"]) > 0 else "nothing"}`
            If a user has any of these roles, the bot will not translate their messages.
            You can enter role mentions, everything else will be ignored.
            To set nothing, include \"nothing\" in the input."""
            # The embed to reply with
            embed = discord.Embed(
                title="Blacklisted Roles",
                description=description,
                color=discord.Color.blue()
            )
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        result, value = await f_blacklisted_roles(value, interaction)

        if result is False:
            return await interaction.followup.send(f"All roles given were invalid, are they correct? Are they in this guild?", ephemeral=True)
        if len(value) == 0:
            return await interaction.followup.send(f'Successfully set "Blacklisted Roles" to `nothing`')

        await interaction.followup.send(f'Successfully updated "Blacklisted Roles" to {", ".join([f"<@&{role_id}>" for role_id in value])}', ephemeral=True)

    async def auto_translate(self, interaction: discord.Interaction,
                            value: bool = None):
        await interaction.response.defer(ephemeral=True)
        
        
        if value is None:
            config = get_guild_config(interaction.guild_id)
            description = f"""Current value: `{"Yes" if config["AUTO_TRANSLATE"] else "No"}`
            Should the bot automatically translate messages"""

            # The embed to reply with
            embed = discord.Embed(
                title="Auto Translate",
                description=description,
                color=discord.Color.blue()
            )
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            
        else:
            # External command
            value = await f_auto_translate(value, interaction)
            await interaction.followup.send(f'Successfully updated "Auto Translate" to `{"Yes" if value else "No"}`', ephemeral=True)

# Setup the commands
async def setup(bot):
    # Add the commands cog
    await bot.add_cog(Config(bot))
