_GOOGLE_TRANSLATE_URL = "https://translate.googleapis.com/translate_a/single"
_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

# A dict of all available languages
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

# A dict for the most common language's country's flag for each language
FLAGS = {
    "af": "<:flag_sa:1347699731433787502>", "sq": "<:flag_al:1347699825881125014>", "am": "<:flag_et:1347699881753710592>", "ar": "<:flag_sar:1347699975642943539>", "hy": "<:flag_ar:1347700042735157348>", "as": "<:flag_in:1347700112905994261>", "ay": "<:flag_bo:1347700695691952260>", "az": "<:flag_az:1347700759898226730>",
    "bm": "<:flag_ma:1347700830660329583>", "eu": "<:flag_sp:1347700887115530390>", "be": "<:flag_be:1347700943986233519>", "bn": "<:flag_ba:1347700994049446011>", "bho": "<:flag_in:1347700112905994261>", "bs": "<:flag_bs:1347701078929703003>", "bg": "<:flag_bu:1347701137196974224>", "ca": "<:flag_sp:1347700887115530390>",
    "ceb": "<:flag_ph:1347876139984490591>", "ny": "<:flag_ch:1347876321082216511>", "zh-cn": "<:flag_ch:1347876321082216511>", "zh-tw": "<:flag_ch:1347876321082216511>", "co": "<:flag_co:1347876633482235905>", "hr": "<:flag_cr:1347876746485043244>", "cs": "<:flag_chre:1347876907923931138>", "da": "<:flag_de:1347877052098809916>",
    "dv": "<:flag_mal:1347877246051815447>", "doi": "<:flag_in:1347700112905994261>", "nl": "<:flag_ne:1347877386447880293>", "en": "<:flag_un:1347877552798175302>", "eo": "<:flag_et:1347699881753710592>", "et": "<:flag_es:1347877681886138379>", "ee": "<:flag_gh:1347877794037895218>", "tl": "<:flag_ph:1347876139984490591>",
    "fi": "<:flag_fi:1347877955657007124>", "fr": "<:flag_fr:1347878068072742923>", "fy": "<:flag_ne:1347877386447880293>", "gl": "<:flag_ge:1347878197500444726>", "ka": "<:flag_geo:1347878350043090965>", "de": "<:flag_ge:1347878197500444726>", "el": "<:flag_gr:1347878494050324550>", "gn": "<:flag_pa:1347878600988426330>", "gu": "<:flag_in:1347700112905994261>",
    "ht": "<:flag_ha:1347990846829625445>", "ha": "<:flag_ni:1347990977281003652>", "haw": "<:flag_un:1347877552798175302>", "iw": "<:flag_is:1347991112958087208>", "hi": "<:flag_in:1347700112905994261>", "hmn": "<:flag_un:1347877552798175302>", "hu": "<:flag_hu:1347991271721009253>", "is": "<:flag_ic:1347991391661330504>",
    "ig": "<:flag_ni:1347990977281003652>", "ilo": "<:flag_ph:1347876139984490591>", "id": "<:flag_ind:1347991514181009568>", "ga": "<:flag_ir:1347991640291409920>", "it": "<:flag_it:1347991748369977414>", "ja": "<:flag_ja:1347991857552163009>", "jw": "<:flag_ind:1347991514181009568>", "kn": "<:flag_in:1347700112905994261>", "kk": "<:flag_kh:1347991982936428596>",
    "km": "<:flag_ca:1347992258149875743>", "rw": "<:flag_rw:1347992371241160898>", "gom": "<:flag_in:1347700112905994261>", "ko": "<:flag_so:1347992502598369350>", "kri": "<:flag_si:1347992610316222675>", "ku": "<:flag_tu:1347992731053719582>", "ckb": "<:flag_ira:1347992870052823040>", "ky": "<:flag_ky:1347993005046370314>", "lo": "<:flag_la:1347993103562440807>",
    "la": "<:flag_va:1347993236177944667>", "lv": "<:flag_lat:1347993393032335481>", "ln": "<:flag_con:1347993679452835950>", "lt": "<:flag_li:1347993916930261123>", "lg": "<:flag_ug:1347994130743038002>", "lb": "<:flag_lu:1347994232798838814>", "mk": "<:flag_no:1347994341682974730>", "mai": "<:flag_in:1347700112905994261>", "mg": "<:flag_mad:1347994482578161775>",
    "ms": "<:flag_mala:1347994635431055391>", "ml": "<:flag_in:1347700112905994261>", "mt": "<:flag_malt:1347995084553191495>", "mi": "<:flag_new:1347995184050470942>", "mr": "<:flag_in:1347700112905994261>", "mni-mtei": "<:flag_in:1347700112905994261>", "lus": "<:flag_in:1347700112905994261>", "mn": "<:flag_mo:1347995316846202950>", "my": "<:flag_my:1347995421938552885>",
    "ne": "<:flag_nep:1347995736993697832>", "no": "<:flag_nor:1347995848763641898>", "or": "<:flag_in:1347700112905994261>", "om": "<:flag_et:1347699881753710592>", "ps": "<:flag_pak:1347996178330947634>", "fa": "<:flag_iran:1347996335583924224>", "pl": "<:flag_po:1347996441011949599>", "pt": "<:flag_br:1347996547693936740>", "pa": "<:flag_in:1347700112905994261>", "qu": "<:flag_pe:1347996721912746024>",
    "ro": "<:flag_ro:1347996872421150770>", "ru": "<:flag_ru:1347996970714660864>", "sm": "<:flag_sam:1347997085122957363>", "sa": "<:flag_in:1347700112905994261>", "gd": "<:flag_sc:1347997239468884061>", "nso": "<:flag_sa:1347699731433787502>", "sr": "<:flag_se:1347997744056504320>", "st": "<:flag_sa:1347699731433787502>", "sn": "<:flag_zi:1347997861710659605>",
    "sd": "<:flag_pak:1347996178330947634>", "si": "<:flag_sr:1347997994607181875>", "sk": "<:flag_sl:1347998228444086463>", "sl": "<:flag_slo:1347998349772722237>", "so": "<:flag_som:1347998524524068946>", "es": "<:flag_sp:1347700887115530390>", "su": "<:flag_ind:1347991514181009568>", "sw": "<:flag_ta:1347997358461554773>", "sv": "<:flag_sw:1347997456071397417>",
    "tg": "<:flag_taj:1347998826732064841>", "ta": "<:flag_in:1347700112905994261>", "tt": "<:flag_ru:1347996970714660864>", "te": "<:flag_in:1347700112905994261>", "th": "<:flag_th:1347998951537905724>", "ti": "<:flag_et:1347699881753710592>", "ts": "<:flag_sa:1347699731433787502>", "tr": "<:flag_tu:1347992731053719582>", "tk": "<:flag_tur:1347999071776014478>",
    "ak": "<:flag_gh:1347877794037895218>", "uk": "<:flag_uk:1347999201878999099>", "ur": "<:flag_pak:1347996178330947634>", "ug": "<:flag_ch:1347876321082216511>", "uz": "<:flag_uz:1347999982212481036>", "vi": "<:flag_vi:1347999308959580210>", "cy": "<:flag_wa:1347999403356721213>", "xh": "<:flag_sa:1347699731433787502>", "yi": "<:flag_un:1347877552798175302>",
    "yo": "<:flag_ni:1347990977281003652>", "zu": "<:flag_sa:1347699731433787502>"
}
