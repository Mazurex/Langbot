_GOOGLE_TRANSLATE_URL = "https://translate.googleapis.com/translate_a/single"
_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

LANGUAGES = {
    'af': 'afrikaans', 'sq': 'albanian', 'am': 'amharic', 'ar': 'arabic', 'hy': 'armenian', 'as': 'assamese', 'ay': 'aymara',
    'az': 'azerbaijani', 'bm': 'bambara', 'eu': 'basque', 'be': 'belarusian', 'bn': 'bengali', 'bho': 'bhojpuri', 'bs': 'bosnian',
    'bg': 'bulgarian', 'ca': 'catalan', 'ceb': 'cebuano', 'ny': 'chichewa', 'zh-cn': 'chinese (simplified)', 'zh-tw': 'chinese (traditional)',
    'co': 'corsican', 'hr': 'croatian', 'cs': 'czech', 'da': 'danish', 'dv': 'dhivehi', 'doi': 'dogri', 'nl': 'dutch', 'en': 'english',
    'eo': 'esperanto', 'et': 'estonian', 'ee': 'ewe', 'tl': 'filipino', 'fi': 'finnish', 'fr': 'french', 'fy': 'frisian', 'gl': 'galician',
    'ka': 'georgian', 'de': 'german', 'el': 'greek', 'gn': 'guarani', 'gu': 'gujarati', 'ht': 'haitian creole', 'ha': 'hausa',
    'haw': 'hawaiian', 'iw': 'hebrew', 'hi': 'hindi', 'hmn': 'hmong', 'hu': 'hungarian', 'is': 'icelandic', 'ig': 'igbo', 'ilo': 'ilocano',
    'id': 'indonesian', 'ga': 'irish', 'it': 'italian', 'ja': 'japanese', 'jw': 'javanese', 'kn': 'kannada', 'kk': 'kazakh', 'km': 'khmer',
    'rw': 'kinyarwanda', 'gom': 'konkani', 'ko': 'korean', 'kri': 'krio', 'ku': 'kurdish (kurmanji)', 'ckb': 'kurdish (sorani)', 'ky': 'kyrgyz',
    'lo': 'lao', 'la': 'latin', 'lv': 'latvian', 'ln': 'lingala', 'lt': 'lithuanian', 'lg': 'luganda', 'lb': 'luxembourgish', 'mk': 'macedonian',
    'mai': 'maithili', 'mg': 'malagasy', 'ms': 'malay', 'ml': 'malayalam', 'mt': 'maltese', 'mi': 'maori', 'mr': 'marathi', 'mni-mtei': 'meiteilon (manipuri)',
    'lus': 'mizo', 'mn': 'mongolian', 'my': 'myanmar', 'ne': 'nepali', 'no': 'norwegian', 'or': 'odia (oriya)', 'om': 'oromo', 'ps': 'pashto',
    'fa': 'persian', 'pl': 'polish', 'pt': 'portuguese', 'pa': 'punjabi', 'qu': 'quechua', 'ro': 'romanian', 'ru': 'russian', 'sm': 'samoan',
    'sa': 'sanskrit', 'gd': 'scots gaelic', 'nso': 'sepedi', 'sr': 'serbian', 'st': 'sesotho', 'sn': 'shona', 'sd': 'sindhi', 'si': 'sinhala',
    'sk': 'slovak', 'sl': 'slovenian', 'so': 'somali', 'es': 'spanish', 'su': 'sundanese', 'sw': 'swahili', 'sv': 'swedish', 'tg': 'tajik',
    'ta': 'tamil', 'tt': 'tatar', 'te': 'telugu', 'th': 'thai', 'ti': 'tigrinya', 'ts': 'tsonga', 'tr': 'turkish', 'tk': 'turkmen',
    'ak': 'twi', 'uk': 'ukrainian', 'ur': 'urdu', 'ug': 'uyghur', 'uz': 'uzbek', 'vi': 'vietnamese', 'cy': 'welsh', 'xh': 'xhosa',
    'yi': 'yiddish', 'yo': 'yoruba', 'zu': 'zulu'
}