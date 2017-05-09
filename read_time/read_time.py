from pelican import signals
from itertools import chain


def init(generator):
    data = {
        'default': {
            'wpm': 200,
            'plurals': [
                'minute',
                'minutes'
            ]
        }
    }

    settings_wpm = generator.settings.get('READ_TIME', data)

    # Allows a wpm entry
    if isinstance(settings_wpm, int):
        data['default']['wpm'] = settings_wpm

    # Default checker
    if isinstance(settings_wpm, dict):
        if 'default' not in settings_wpm:
            return None
        if 'wpm' not in settings_wpm['default']:
            return None
        if 'plurals' not in settings_wpm['default']:
            return None
        if not isinstance(settings_wpm['default']['wpm'], int):
            return None
        if not isinstance(settings_wpm['default']['plurals'], list):
            return None
        if len(settings_wpm['default']['plurals']) != 2:
            return None
        data = settings_wpm

    for article in chain(generator.articles, generator.drafts, generator.translations, generator.drafts_translations):
        language = 'default'
        if article.lang in data:
            language = article.lang
        # Exit if read time is set by article
        if hasattr(article, 'read_time'):
            return None

        article.read_time = calculate_wpm(article.content, data, language)
        article.read_time_string = generate_string(
            article.read_time, data, language)

def calculate_wpm(text, data, language):
    '''
    Calculates read length of article
    '''

    try:
        wpm = data[language]['wpm']
    except LookupError:
        wpm = data['default']['wpm']

    read_time = len(text.split(' ')) / wpm

    # Articles cannot take 0 minutes to read
    if read_time == 0:
        return 1

    return read_time


def generate_string(read_time, data, language):
    '''
    Generates read length as string with appropriate plurality i.e 1 minute, 4 minutes
    '''

    try:
        non_plural = data[language]['plurals'][0]
    except LookupError:
        non_plural = data['default']['plurals'][0]

    try:
        plural = data[language]['plurals'][1]
    except LookupError:
        plural = data['default']['plurals'][1]

    if read_time != 1:
        return '{0} {1}'.format(read_time, plural)

    return '{0} {1}'.format(read_time, non_plural)


def register():
    signals.article_generator_finalized.connect(init)
