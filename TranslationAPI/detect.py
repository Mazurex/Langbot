import requests

from TranslationAPI.constants import _HEADERS, _GOOGLE_TRANSLATE_URL


def detect(source: str) -> str | None:
    """Detect a language from a given source using the Google API"""
    # Params for the GET request
    params = {
        "client": "gtx",
        "sl": "auto",
        "tl": "en",
        "dt": "t",
        "q": source,
    }

    try:
        # Send a GET request
        response = requests.get(_GOOGLE_TRANSLATE_URL, params=params, headers=_HEADERS)
        response.raise_for_status()

        # Get the detected language
        return response.json()[2]
    except requests.exceptions.RequestException:
        # Error: Return None
        return None