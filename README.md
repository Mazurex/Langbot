# 🌎 LangBot

A powerful and open source Discord bot, **LangBot** is aimed at stopping the language barrier we experience in large Discord servers, members may want to speak other languages, however they are not allowed to, as it's hard for moderators to... moderate. So I came up with a Discord bot, that instantly replies to a message with a translation and language of origin. Want to translate something secretly? Well you can with the `/translate <prompt> (language)` command, where you enter a prompt in **any** language, and the bot will translate it for you into your desired language (**en** by default), where only you can see it!

## Features

- **Simple** - The source code is well commented, aimed at making it easier to understand.
- **Fast** - The bot works asynchronously, allowing multiple operations at the same time.
- **Configurable** - Admins can configure features in their guild with the `/config` command.
- **Reliable** - The bot uses Google Translate's API for translation, meaning it is as reliable as google translate.

## How It Works

**LangBot** interacts with the Discord API using [discord.py](https://discordpy.readthedocs.io/en/stable/), allowing for blazing fast communication, and simplicity within the source code. Translation is done with the [googletrans](https://pypi.org/project/googletrans/) Python Library, allowing for reliable and stable translation. The customizable config is held on a **MongoDB** server, meaning it is secure. You are able to customize the translation message, by default being: `{flag} ➜ {translated}` which looks like this: `🇩🇪 ➜ Hello World` (flag is shown in Discord), with lots of placeholders you are able to customize this message to your liking. The automatic translation feature looks at the guild's config for the `target language` and `ignored language(s)`, if any message is not meant to be ignored, it will be translated into the `target language`, meaning you can customize what languages the bot should ignore, and what language to translate to. The `/translate` command uses the exact same system, however only processing when the command is called, rather than every message it sees. All inputs that may require a language, such as the `(language)` parameter in `/translate` can either be the language code (such as `en`) or the language name (such as `English`).

## Commands

### 🈹 Translate (`/translate <prompt> (language)`)

**Description:**
This command allows users to secretly translate messages into any language.

**Usage:**

```
/translate <prompt> (language)
```

**How It Works:**

1. The bot checks if the user specified a language, if they did, ensure it is valid, if the use doesn't specify a language, it will default to the guild's config target language.
2. Then the bot determines what language the `<prompt>` is in.
3. It then translates the message using the `(language)` parameter.

**Example:**

```
User: /translate ja jestem polski
Bot (Private Reply): [Polish ➜ English]
                     I am Polish
```

[TRANSLATION COMMAND IMAGE]

---

### All Supported Languages (`/supported`)

**Description:**
Fetches a list of **all** supported languages from the **googletrans** library, and places them in a paginated embed.

**Usage:**

```
/supported
```

**How It Works:**

1. The bot gets a Python dictionary of all supported languages from the **googletrans** library.
2. Then the bot paginates these languages (as there are over 300) into 30 languages per page.
3. It then sends an embed with buttons to travel through the pages.

**Example:**

```
/supported
```

[SUPPORTED COMMAND IMAGE]

---

### Admin Command: Configure The Bot (`/config {subcommand ?(value)}`)

**Description:**
Allows the configuration of the bot in the guild, such as translation reply formats, target and ignored languages and other settings, the `/config` command is just a parent command, housing a list of `subcommands`, which may or may not have an optional `value` parameter (`?` as the parameter may not exist for some subcommands), leaving the value parameter blank will display the current setting and information about that configuration option. Here's a list of subcommands:

1. `/config view` - View all current configurations, with a description for each one.
2. `/config reset` - Reset the guild's configurations to their default values.
3. `/config translation-reply-message (value)` - Change the message that the bot replies with on translation, the `value` parameter accepts placeholders, here's a list of all placeholders:
   1. `{flag}` - The flag of the untranslated languages country.
   2. `{translated}` - The translated message.
   3. `{original}` - The original untranslated message.
   4. `{author_id}` - The ID of the author of the message.
   5. `{guild_id}` - The ID of the guild of the message.
   6. `{lang_code}` - The language code of the untranslated message (for example: `en`).
   7. `{lang_name}` - The language name of the untranslated message (for example: `English`).
4. `/config target-language (value)` - Change the language that the bot will translate messages into when replying, must be a valid language (check `/supported`).
5. `/config ignore-languages (value)` - A list of languages to ignore, separated by commas (for example: `en, de, fr`).
6. `/config ignore-bots (value)` - A true or false statement, if `false` the bot will translate messages from other bots (if their languages are not in the ignored list).

**Usage:**

```
/config view
/config reset
/config translation-reply-message {flag} >>> {translated}
/config target-language en
/config ignore-languages en, fr, de
/config ignore-bots true
```

**Default Values:**

1. Translation reply message: `{flag} ➜ {translated}`
2. Target Language: `en`
3. Ignore Languages: `en`
4. Ignore Bots: `true`

---

## Installation & Setup

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

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

- **Discord Server**: [Invite Link](https://discord.gg/AYmdn5UuwJ)
- **GitHub Issues**: [Report Bugs](https://github.com/Mazurex/Langbot/issues)
- **Email**: business.mazurex@gmail.com
