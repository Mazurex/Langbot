import discord
from discord import app_commands
from discord.ext import commands
from db.config_manager import (
    get_guild_config,
    set_channel_config,
    remove_channel_config,
)
from utils.utils import internal_print_log_message

# All customize commands here have an option value parameter
# If no value is given, instead send an embed for what the command does


def description():
    """Embed description"""
    return """Alongside the guild-wide config, you can also create a custom config for every channel.
The parameters for creating a channel config uses the same logic as using `/config {x}`.
If you don't specify a value for a parameter when setting, it will just take the value from the server-wide config value.
"""


class ChannelConfigPaginator(discord.ui.View):
    """Paginated view for cycling through channel-specific configurations"""

    def __init__(self, user: discord.Member, channel_configs: dict):
        super().__init__()
        self.user = user
        self.channel_configs = list(channel_configs.items())
        self.current_page = 0
        self.total_pages = len(self.channel_configs)

    def format_page(self):
        """Formats the embed for the current channel config page"""
        channel_id, config = self.channel_configs[self.current_page]

        embed = discord.Embed(
            title=f"Channel Based Config View {self.current_page + 1}/{self.total_pages}",
            description=description(),
            color=discord.Color.blue(),
        )

        embed.add_field(
            name="Channel ID", value=f"`{channel_id}` (<#{channel_id}>)", inline=False
        )
        embed.add_field(
            name="Translation Reply Message",
            value=f"`{config.get('TRANSLATE_REPLY_MESSAGE', 'N/A')}`",
            inline=False,
        )
        embed.add_field(
            name="Target Language",
            value=f"`{config.get('TARGET_LANG', 'N/A')}`",
            inline=False,
        )
        embed.add_field(
            name="Ignored Languages",
            value=f"`{', '.join(config.get('IGNORE_LANGS', []))}`",
            inline=False,
        )
        embed.add_field(
            name="Ignore Bots",
            value=f"`{config.get('IGNORE_BOTS', False)}`",
            inline=False,
        )
        embed.add_field(
            name="Blacklisted Terms",
            value=f"`{', '.join(config.get('BLACKLISTED_TERMS', []))}`",
            inline=False,
        )

        return embed

    async def update_message(self, interaction: discord.Interaction):
        """Updates the embed when a button is clicked"""
        embed = self.format_page()
        await interaction.response.edit_message(embed=embed, view=self)

    async def interaction_check(self, interaction: discord.Interaction):
        """Ensures only the command author can use the buttons"""
        return interaction.user == self.user

    @discord.ui.button(label="<", style=discord.ButtonStyle.blurple)  # type: ignore
    async def previous_page(
        self, interaction: discord.Interaction, button=discord.ui.Button
    ):
        """Go to the previous page"""
        if self.current_page > 0:
            self.current_page -= 1
        else:
            self.current_page = self.total_pages - 1
        await self.update_message(interaction)

    @discord.ui.button(label=">", style=discord.ButtonStyle.blurple)  # type: ignore
    async def next_page(
        self, interaction: discord.Interaction, button=discord.ui.Button
    ):
        """Go to the next page"""
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
        else:
            self.current_page = 0
        await self.update_message(interaction)


class Channel_config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.config = app_commands.Group(
            name="channel-config",
            description="Channel based configuration",
            default_permissions=discord.Permissions(administrator=True),
        )
        self.config.command(
            name="view",
            description="View information and current configurations related to this command",
        )(self.view)
        self.config.command(
            name="set",
            description="Set a channel based configuration, empty values will be set as the guild-wide config value",
        )(self.set)
        self.config.command(
            name="remove", description="Remove a channel based configuration"
        )(self.remove)

        self.bot.tree.add_command(self.config)

    async def view(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        config = await get_guild_config(interaction.guild_id)  # type: ignore
        channel_config = config.get("CHANNEL_CONFIG")

        if not channel_config:
            embed = discord.Embed(
                title=f"Channel Based Config View",
                description=description(),
                color=discord.Color.blue(),
            )
            return await interaction.followup.send(embed=embed, ephemeral=True)

        view = ChannelConfigPaginator(interaction.user, channel_config)  # type: ignore
        embed = view.format_page()

        await interaction.followup.send(embed=embed, view=view, ephemeral=True)
        internal_print_log_message(interaction, "channel-config/view")

    @app_commands.describe(channel="The channel to set")
    @app_commands.describe(
        translate_reply_message="The message to send when replying with a translation"
    )
    @app_commands.describe(target_language="The language to translate to")
    @app_commands.describe(
        ignore_languages="The languages to ignore, separate with commas"
    )
    @app_commands.describe(
        ignore_bots="Should the bot ignore other bots messages when looking for translations"
    )
    @app_commands.describe(
        blacklisted_terms="Terms that the bot will remove from a message, separate with commas"
    )
    @app_commands.describe(reply="Should the bot reply to the untranslated message")
    @app_commands.describe(
        blacklisted_roles="Any members with these roles will be ignored by the bot, type * to disable"
    )
    @app_commands.describe(
        auto_translate="Should the bot automatically translate messages"
    )
    async def set(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        translate_reply_message: str | None = None,
        target_language: str | None = None,
        ignore_languages: str | None = None,
        ignore_bots: bool | None = None,
        blacklisted_terms: str | None = None,
        reply: bool | None = None,
        blacklisted_roles: str | None = None,
        auto_translate: bool | None = None,
    ):
        await interaction.response.defer(ephemeral=True)

        channel_config = await set_channel_config(
            interaction.guild_id,  # type: ignore
            channel.id,  # type: ignore
            translate_reply_message,
            target_language,
            ignore_languages,  # type: ignore
            ignore_bots,  # type: ignore
            blacklisted_terms,  # type: ignore
            reply,  # type: ignore (python bugging like usual)
            blacklisted_roles,  # type: ignore
            auto_translate,
        )  # type: ignore

        ignored_languages_str = "none"
        if len(channel_config["IGNORED_LANGS"]) > 0:
            ignored_languages_str = ", ".join(channel_config["IGNORE_LANGS"])

        blacklisted_terms_str = "none"
        if len(channel_config["BLACKLISTED_TERMS"]) > 0:
            blacklisted_terms_str = ", ".join(channel_config["BLACKLISTED_TERMS"])

        blacklisted_roles_str = "none"
        if len(channel_config["BLACKLISTED_ROLES"]) > 0:
            blacklisted_roles_str = ", ".join(
                [f"<@&{role_id}>" for role_id in channel_config["BLACKLISTED_ROLES"]]
            )

        description = f"""Successfully set a channel config for <#{channel.id}>.
        Translation reply message: `{channel_config["TRANSLATE_REPLY_MESSAGE"]}`
        Target Language: `{channel_config["TARGET_LANG"]}`
        Ignored Languages: `{ignored_languages_str}`
        Ignore Bots: `{"Yes" if channel_config["IGNORE_BOTS"] else "No"}`
        Ignored Terms: `{blacklisted_terms_str}`
        Reply: `{"Yes" if channel_config["REPLY"] else "No"}`
        Blacklisted Roles: `{blacklisted_roles_str}`
        Auto Translate: `{auto_translate}`"""

        await interaction.followup.send(description, ephemeral=True)
        internal_print_log_message(interaction, "channel-config/set")

    @app_commands.describe(channel="The channel to remove the configuration from")
    async def remove(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ):
        await interaction.response.defer(ephemeral=True)

        removed = await remove_channel_config(interaction.guild_id, channel.id)  # type: ignore

        if not removed:
            return await interaction.followup.send(
                f"<#{channel.id}> does not have a channel config to remove!",
                ephemeral=True,
            )
        else:
            await interaction.followup.send(
                f"Successfully deleted the channel config for <#{channel.id}>"
            )
        internal_print_log_message(interaction, "channel-config/remove")


async def setup(bot):
    await bot.add_cog(Channel_config(bot))
