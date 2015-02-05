from datetime import date
from pelican import signals


def draftfuture(article_generator, metadata=None):
    if 'date' in metadata and metadata['date'].date() > date.today():
        metadata['status'] = 'draft'
        drafts = article_generator.context.setdefault('drafts', [])
        if metadata not in drafts:
            drafts.append(metadata)


def register():
    signals.article_generator_context.connect(draftfuture)
