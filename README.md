# 🌎 LangBot

A powerful and open source Discord bot, **LangBot** is aimed at stopping the language barrier we experience in large Discord servers, members may want to speak other languages, however they are not allowed to, as it's hard for moderators to... moderate. So I came up with a Discord bot, that instantly replies to a message with a translation and language of origin. Want to translate something secretly? Well you can with the `/translate <prompt> (language)` command, where you enter a prompt in **any** language, and the bot will translate it for you into your desired language (**en** by default), where only you can see it!

## Guild Setup

Adding **LangBot** to your guild is very straightforward, as the bot is very plug-and-play, with all configs preset with default values.

1. [Invite](https://discord.com/oauth2/authorize?client_id=1341595906662993920&permissions=3072&integration_type=0&scope=bot+applications.commands) the bot to your server.
2. The bot needs very few permissions, "Send Messages" and "View Channels."
3. If you would like to customize your config, look at the [Admin Commands](#admin-commands) section.
4. And you're done!

## Features

- **Simple** - The source code is well commented, aimed at making it easier to understand.
- **Fast** - The bot works asynchronously, allowing multiple operations at the same time.
- **Configurable** - Admins can configure features in their guild with the `/config` command.
- **Reliable** - The bot uses Google Translates API for translation, meaning it is as reliable as Google Translate.

## How It Works

**LangBot** interacts with the Discord API using [discord.py](https://discordpy.readthedocs.io/en/stable/), allowing for blazing fast communication, and simplicity within the source code. Translation is done with custom functions, allowing for reliable and stable translation. The customizable config is held on a **MongoDB** server, meaning it is secure. You are able to customize the translation message, by default being: `{flag} ➜ {translated}` which looks like this: `🇩🇪 ➜ Hello World` (flag is shown in Discord), with lots of placeholders you are able to customize this message to your liking. The automatic translation feature looks at the channel-based or guild-based config for the `target language` and `ignored language(s)`, if any message is not meant to be ignored, it will be translated into the `target language`, meaning you can customize what languages the bot should ignore, and what language to translate to. The `/translate` command uses the exact same system, however only processing when the command is called, rather than every message it sees. All inputs that may require a language, such as the `(language)` parameter in `/translate` can either be the language code (such as `en`) or the language name (such as `English`).

## Commands

### Translate (`/translate <prompt> (language)`)

**Description:**
This command allows users to secretly translate messages into any language.

**Usage:**

```
/translate <prompt> (language)
```

**How It Works:**

1. The bot checks if the user specified a language, if they did, ensure it is valid, if the user doesn't specify a language, it will default to the guild's config target language.
2. Then the bot determines what language the `<prompt>` is in.
3. It then translates the message using the `(language)` parameter.

**Example:**

```
User: /translate ja jestem polski
Bot (Private Reply): [Polish ➜ English]
                     I am Polish
```

# ![image](https://github.com/user-attachments/assets/c6647786-a7a6-4857-82b5-a9b8301cd8be)

---

### All Supported Languages (`/supported`)

**Description:**
Fetches a list of **all** supported languages from a custom dictionary, and places them in a paginated embed.

**Usage:**

```
/supported
```

**How It Works:**

1. The bot gets a Python dictionary of all supported languages from a custom dictionary.
2. Then the bot paginates these languages (as there are over 300) into 30 languages per page.
3. It then sends an embed with buttons to travel through the pages.

**Example:**

```
/supported
```

# ![image](https://github.com/user-attachments/assets/3d41c5da-0019-4e0b-9f98-60c0696d17c8)

---

## Admin Commands

### Configure The Bot (`/config {subcommand ?(value)}`)

**Description:**
Allows the configuration of the bot in the guild, such as translation reply formats, target and ignored languages and other settings, the `/config` command is just a parent command, housing a list of `subcommands`, which may or may not have an optional `value` parameter (`?` as the parameter may not exist for some subcommands), leaving the value parameter blank will display the current setting and information about that configuration option. NOTE: the reset subcommand will also wipe all channel-based configs! Here's a list of subcommands:

1. `/config view` - View all current configurations, with a description for each one.
2. `/config reset` - Reset the guild's configurations to their default values.
3. `/config translation-reply-message (value)` - Change the message that the bot replies with on translation, the `value` parameter accepts placeholders, here's a list of all placeholders:
   1. `{flag}` - The flag of the untranslated languages country.
   2. `{translated}` - The translated message.
   3. `{original}` - The original untranslated message.
   4. `{author_id}` - The ID of the author of the message.
   5. `{author_display_name}` - The display name of the author of the message.
   6. `{author_username}` - The username of the author of the message.
   7. `{author_mention}` - Mention the author of the message.
   8. `{author_avatar}` - The avatar of the author of the message.
   9. `{guild_id}` - The ID of the guild of the message.
   10. `{guild_name}` - The name of the guild of the message.
   11. `{channel_id}` - The ID of the channel of the message.
   12. `{channel_name}` - The name of the channel of the message.
   13. `{message_id}` - The ID of the original untranslated message.
   14. `{message_url}` - The URL to the original untranslated message.
   15. `{lang_code}` - The language code of the untranslated message (for example: `en`).
   16. `{lang_name}` - The language name of the untranslated message (for example: `English`).
4. `/config target-language (value)` - Change the language that the bot will translate messages into when replying, must be a valid language (check `/supported`).
5. `/config ignore-languages (value)` - A list of languages to ignore, separated by commas (for example: `en, de, fr`). Only enter "nothing" to disable this.
6. `/config ignore-bots (value)` - A true or false statement, if `false` the bot will translate messages from other bots (if their languages are not in the ignored list).
7. `/config ignored-terms (value)` - A list of words that are not allowed to be translated, if the translated message contains one of these, it will not be translated. Only enter "nothing" to disable this.
8. `/config reply (value)` - A true of false statement, if `false` the bot will send the message in the channel, otherwise it will reply to the untranslated message.
9. `/config ignored-roles (value)` - A list of @mentions, if a user has any of these mentions, they will be blocked by automatic translation. Only enter "nothing" to disable this.
10. `/config blacklisted-roles (value)` - A list of @mentions, if a user has any of these mentions, they will be blocked by automatic translation. Only enter "nothing" to disable this.
11. `/config auto-translate (value)` - If false the bot will ignore any message, regardless of the language its spoken in.

**Usage:**

```
/config view
/config reset
/config translation-reply-message {flag} >>> {translated}
/config target-language en
/config ignore-languages en, fr, de
/config ignore-bots true
/config ignored-terms hello, world
/config reply false
/config ignored-roles @owner @coolguy
=======
/config blacklisted-roles @owner @coolguy
/config auto-translate true
```

**Default Values:**

1. Translation reply message: `{flag} ➜ {translated}`
2. Target Language: `en`
3. Ignore Languages: `en`
4. Ignore Bots: `true`
5. Ignored Terms: `"lmaoo", "wdym", "ik", "ik lol"`
6. Reply: `true`
7. # Ignored Roles: `none`
8. Blacklisted Roles: `none`
9. Auto Translate: `true`

![image](https://github.com/user-attachments/assets/c1a3fe5c-d7fa-484d-9e30-55e9a6d5fce1)

---

### Channel-Based configs (`/channel-config {subcommand ?(value(s))}`)

**Description:**
This is an extension to the original guild-based config, it allows for channels to have custom configurations, alongside the guild-based one, meaning that you can have your main guild-based config as a default, and then set a few channels to contain other configuration options, outside the default config, allowing you to have other language channels, which can translate into that channels language. All (other than channel) parameters in set are optional, see default values. Here's a list of subcommands:

1. `/channel-config view` - View all channel configurations as a paginated list, alongside information regarding channel configs.
2. `/channel-config set {channel} (values)` - Set a channel config for a specific channel, the parameters will match the `/config` parameters.
3. `/channel-config remove {channel}` - Remove a channel configuration from a specific channel.

**Usage:**

```
/channel-config view
/channel-config set #general translate_reply_message = "{translated} = {flag}" ignore_languages = en,fr
/channel-config remove #general
```

**Default Values:**

On the set subcommand, all parameters, besides `channel` are optional, and if left blank, it will set the value to the value in the guild-based config.

![image](https://github.com/user-attachments/assets/c1a3fe5c-d7fa-484d-9e30-55e9a6d5fce1)

![image](https://github.com/user-attachments/assets/c1a3fe5c-d7fa-484d-9e30-55e9a6d5fce1)

---

## Installation & Setup

This bot is open-source, meaning you are able to clone this repository and play around with it yourself, however, under the laws of the **Prosperity Public License** agreements, you may **NOT** distribute, sublicense or publically share any part of this software without my written approval.

1. **Clone the repository**
   ```sh
   git clone https://github.com/Mazurex/Langbot.git
   cd LangBot
   ```
2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
3. **Configure environment variables**
   - Rename `.env.example` to `.env` and fill in your bot token & MongoDB URI
   - Ensure you have a MongoDB database set up. You can use [MongoDB Atlas](https://www.mongodb.com/atlas/database) (cloud-based) or run MongoDB locally.
4. **Run the bot**
   ```sh
   python -m bot.main
   ```

## Donations

Love the bot? Consider supporting development with a donation!

- [Buy Me a Coffee](https://ko-fi.com/mazurex)

## Contributing

Want to contribute? Follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature-branch`)
3. Commit changes (`git commit -m "Added a new feature"`)
4. Push to your branch (`git push origin feature-branch`)
5. Open a Pull Request

## License

This project is licensed under the Prosperity Public License—see the [LICENSE](LICENSE) file for details.

## Contact

- **Discord Server**: [Invite Link](https://discord.gg/AYmdn5UuwJ)
- **GitHub Issues**: [Report Bugs](https://github.com/Mazurex/Langbot/issues)
- **Email**: business.mazurex@gmail.com

## Credits

- [Mazurex](https://www.youtube.com/channel/UCQgCmVILYg6AfsohPTxrQPg) - Developer, Tester
- [Azy Supreme](https://www.youtube.com/channel/UCPQGu1pokNERNJVZkZdl7-A) - Tester
- [codingcat](https://codingcat24.dev/) - Tester
- [Random_Chad](https://store.basement.host/) - Tester
