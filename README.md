# Introduction

---

**LangBot** is a Discord bot made using `discord.py`, it servers a small purpose, automatic translation, one issue for most big discord servers, is the language barrier, some users may want to talk in other languages, but they cannot, with **LangBot** they can!
The bot uses the `googletrans` library, which uses AI for translation (meaning results may not always be accurate).

# How it works

---

There are 2 translation features for **LangBot**:

1.  Automatic translation.
2.  Command translation.

## Automatic Translation

The bot connects to a database, looking for the specific entry for that guild (creating a default one if it doesn't exist). The bot then reads every message sent, it then determines whether to translate that message based on the given configuration, if it decides to translate, it will reply the the message with the translated version, with a customizable format with placeholders (explained later).

## Command Translation

The bot also has a `/translate <prompt> (language)` command, where you are able to easily and privately translate any message into any supported language, by default `language` is set to "en", meaning it will translate to English, you can change this to any language code or name!

# Commands

---

`/config {sub ?<value>}` - The config command allows you to customize lots of aspects of the bot in your guild, the `{}` symbolizes a sub-command, the `?` symbolizes that a value may or may not exist for that sub-command.

One sub-command is `view` (`/config view`), this sends an embed message with the guilds configurations.

Another sub-command is `reset` (`/config reset`), this command resets your guilds configurations to their default values.
Then there are subcommands specific to aspects of the bot, the value is optional for all these aspects, if you don't specify a value, the bot will instead send an embed with information regarding that option.
All config commands are `Admin` ONLY, meaning regular users cannot modify them.

# Extra

---

This project is **completely** open-source, you may modify and improve it as you wish, this project was made for learning, meaning everything is public regarding this bot (other than the sensitive stuff).

If you do want to donate, you may do so at my KoFi: https://ko-fi.com/mazurex.
If you encounter any bugs, let me know in my discord server: https://discord.gg/AYmdn5UuwJ.
