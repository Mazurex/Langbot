from typing import Literal, Tuple

import requests

from i_logger.logger import log

from TranslationAPI.constants import _HEADERS, _GOOGLE_TRANSLATE_URL, LANGUAGES

def translate(source: str, target_lang: str = "en", source_lang: Literal["auto"] | str = "auto") -> Tuple[str, str]:
    """Function to translate a given source using the Google API"""
    # Not a valid language code
    if target_lang not in LANGUAGES.keys():
        # Not a valid language name
        if target_lang not in LANGUAGES.values():
            log("Target language {target_lang} is not a valid language", "critical")
        else:
            # Convert language name to language code
            target_lang = {v: k for k, v in LANGUAGES.items()}[target_lang]

    # Not a valid language code and not equal to "auto"
    if source_lang not in LANGUAGES.keys() and source_lang != "auto":
        # Not a valid language name
        if source_lang not in LANGUAGES.keys():
            log("Target language {target_lang} is not a valid language", "critical")
        else:
            # Convert language name to code
            source_lang = {v: k for k, v in LANGUAGES.items()}[source_lang]

    # Params for GET request
    params = {
        "client": "gtx",
        "sl": source_lang,
        "tl": target_lang,
        "dt": "t",
        "q": source,
    }

    try:
        # Send the GET request
        response = requests.get(_GOOGLE_TRANSLATE_URL, params=params, headers=_HEADERS)
        response.raise_for_status()

        # Get the translated text
        translated_text = " ".join(item[0] for item in response.json()[0] if item[0])

        return translated_text, response.json()[2].lower()
    except:
        # Error: Return the original source message
        return source, source_lang