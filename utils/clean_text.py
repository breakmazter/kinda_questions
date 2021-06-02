from urlextract import URLExtract
import re
import emoji

import warnings
warnings.filterwarnings("ignore")

extractor = URLExtract()

uchr = chr  # Python 3

_removable_emoji_components = (
    (0x20E3, 0xFE0F),             # combining enclosing keycap, VARIATION SELECTOR-16
    range(0x1F1E6, 0x1F1FF + 1),  # regional indicator symbol letter a..regional indicator symbol letter z
    range(0x1F3FB, 0x1F3FF + 1),  # light skin tone..dark skin tone
    range(0x1F9B0, 0x1F9B3 + 1),  # red-haired..white-haired
    range(0xE0020, 0xE007F + 1),  # tag space..cancel tag
)
emoji_components = re.compile(u'({})'.format(u'|'.join([
    re.escape(uchr(c)) for r in _removable_emoji_components for c in r])),
    flags=re.UNICODE)


def normalize_spacing_for_tok(text: str) -> str:
    res = (
        text.replace("\r", "")
        .replace("(", " (")
        .replace(")", ") ")
        .replace(" +", " ")
    )
    res = re.sub(r"\) ([\.\!\:\?\;\,])", r"\)\1", res)
    res = res.replace("( ", "(").replace(" )", ")")
    res = re.sub(r"(\d) \%", r"\1\%", res)
    res = res.replace(" :", ":").replace(" ;", ";")
    res = res.replace("`", "'").replace("''", ' " ')

    res = (
        res.replace("„", '"')
        .replace("“", '"')
        .replace("”", '"')
        .replace("–", "-")
        .replace("—", "-")
        .replace(" +", " ")
        .replace("´", "'")
        .replace("‘", '"')
        .replace("''", '"')
        .replace("´´", '"')
        .replace("…", "...")
        .replace(" « ", ' "')
        .replace("« ", '"')
        .replace("«", '"')
        .replace(" » ", '" ')
        .replace(" »", '"')
        .replace("»", '"')
        .replace(" %", "%")
        .replace("nº ", "nº ")
        .replace(" :", ":")
        .replace(" ºC", " ºC")
        .replace(" cm", " cm")
        .replace(" ?", "?")
        .replace(" !", "!")
        .replace(" .", ".")
        .replace(" ,", ",")
        .replace(" ;", ";")
        .replace(", ", ", ")
        .replace(" +", " ")
        .replace("．", ". ")
        .replace(".", ". ")
        .replace(",", ", ")
        .replace("!", "! ")
        .replace("?", "? ")
    )

    return res


def replace_tags(text: str) -> str:
    """Replace all tags from a given text with ' '.
    A tag is a string formed by @ concatenated with a sequence of characters
    and digits. Example: @texthero123.
    Parameters
    ----------
    text : str
        Text to clean from tags
    """

    pattern = r"@\S+"
    return re.sub(pattern, ' ', text)


def replace_hashtags(text: str) -> str:
    """Replace all hashtags from a text with ' '
    A hashtag is a string formed by # concatenated with a sequence of
    characters, digits and underscores. Example: #texthero_123.
    Parameters
    ----------
    text : str
        Text to clean from hashtags
    """
    pattern = r"#\S+"
    return re.sub(pattern, ' ', text)


def replace_bad_words(text):
    bad = [
        'instagram', 'facebook', 'youtube', 'twitter', 'github', 'linkedin', 'vkontakte', 'telegram' 'android'
    ]
    return re.sub('|'.join(bad), ' ', text)


def replace_emoji(text):
    text = emoji_components.sub(u' ', emoji.get_emoji_regexp().sub(u' ', text))

    text = re.compile("["
                      u"\U0001F600-\U0001F64F"
                      u"\U0001F300-\U0001F5FF"
                      u"\U0001F680-\U0001F6FF"
                      u"\U0001F1E0-\U0001F1FF"
                      u"\U00002702-\U000027B0"
                      u"\U00010000-\U0010ffff"
                      U"\U000020A0-\U00002BFF"
                      U"\U0000FE00-\U0000FE0F"
                      # u"\U000024C2-\U0001F251"
                      "]+", flags=re.UNICODE).sub(r' ', text)
    return text


def replace_urls_emails(text):
    text = text.replace('http', ' http')
    for url in sorted(extractor.find_urls(text, only_unique=True), reverse=True):
        text = text.replace(url, ' ')

    pattern = re.compile('([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)')
    text = re.sub(pattern, ' ', text)
    return text


def replace_bad_symbols(text):
    text = text.replace('\u200b', ' ')
    text = text.replace('\xad', ' ')
    # NON_PRINTING_CHAR
    text = re.compile(
        f"[{''.join(map(chr, list(range(0, 32)) + list(range(127, 160))))}]"
    ).sub(r' ', text)
    return text


def replace_brackets_with_content(text):
    text = re.sub("[\(\[\{].*?[\)\]\}]", " ", text)
    return text


def replace_repeated_punct(text):
    pattern = re.compile(r'([,.!?:;"+*$|\-—=#"_]){2,}')
    text = re.sub(pattern, ' ', text)

    pattern = re.compile(r'([\s]){2,}')
    text = re.sub(pattern, ' ', text)
    return text


def replace_spaces(text):
    text = text.replace('\n', ' ')
    text = text.replace('\\n', ' ')
    text = text.replace('\r', ' ')
    text = text.replace('\\r', ' ')
    text = text.replace('\t', ' ')
    text = text.replace('\\t', ' ')
    return text


def replace_smth(text):
    text = re.sub(r'\s\d+([.,:;+*\-+=]\d+)?[\s\W]', ' ', text)
    return text


def replace_useless_punct(text):
    text = text.replace('|', '.')
    text = text.replace('•', ' ')
    text = text.replace('~', ' ')
    text = text.replace('#', ' ')
    text = text.replace(' - ', ' ')
    text = text.replace('/', ' ')
    text = text.replace('・', ' ')
    text = text.replace('=', ' ')
    text = text.replace('_', ' ')
    text = text.replace('%', ' ')
    text = text.replace('&', ' ')
    text = text.replace(' —', ' ')
    return text


def replace_repeated_whitespaces(text) -> object:
    text = re.sub(r'\d', ' ', text)
    text = re.sub('\s+', ' ', text)
    return text


# TODO remove Personal names
def clean_text(text):
    if text:
        text = replace_bad_symbols(text)

        text = replace_emoji(text)

        text = replace_urls_emails(text)

        text = replace_bad_words(text)

        text = text.lower()

        text = replace_brackets_with_content(text)

        text = replace_hashtags(text)

        text = replace_tags(text)

        text = replace_repeated_punct(text)

        text = replace_spaces(text)

        text = replace_smth(text)

        text = replace_useless_punct(text)

        text = normalize_spacing_for_tok(text)

        text = replace_repeated_whitespaces(text)

        text = text.strip()
    else:
        text = None
    return text
