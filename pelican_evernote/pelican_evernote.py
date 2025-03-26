from pelican import signals
from evernote.api.client import *
from evernote.edam.error.ttypes import TException, EDAMUserException
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec
from operator import itemgetter
from markdownify import markdownify as md
from datetime import datetime
import os.path
import logging
logger = logging.getLogger(__name__)


class EvernoteNotes(object):
    mandatory_credentials = ['EVERNOTE_CONSUMER_KEY', 'EVERNOTE_CONSUMER_SECRET', 'EVERNOTE_TOKEN']

    filter_words = 'EVERNOTE_FILTER_WORDS'

    evernote_article_folder = 'EVERNOTE_ARTICLE_FOLDER'

    evernote_note_prefix = 'evnote'

    client = None

    settings = None

    notes = []

    def __init__(self, settings):
        self.validate_credentials(settings)
        self.settings = settings
        self._init_client(*itemgetter(*self.mandatory_credentials)(settings))
        self._test_connection()

    def _test_connection(self):
        if not self.client.get_user_store().getUser():
            raise UserWarning('Can not connect to Evernote')

    def write_all_articles(self):
        for note_list in self._generate_notes_list():
            for guid, note in note_list:
                with open(self.get_evernote_article_path() + self.evernote_note_prefix + guid + '.md', 'w') as holder:
                    holder.write(note)

    def validate_credentials(self, settings):
        for cred in self.mandatory_credentials:
            if cred not in settings.keys():
                raise UserWarning('Missing mandatory credential ' + cred)
        return True

    def _turn_note_into_article(self, note_guid, note_store):
        md_note = ''
        note = note_store.getNote(self.client.token, note_guid, True, True, True, True)
        note_tags = note_store.getNoteTagNames(self.client.token, note_guid)
        md_note += 'Title: %s \n' % note.title
        md_note += 'Date: %s \n' % datetime.fromtimestamp(note.created / 1e3).strftime('%Y-%m-%d %H:%M')
        md_note += 'Modified: %s \n' % datetime.fromtimestamp(note.updated / 1e3).strftime('%Y-%m-%d %H:%M')
        md_note += 'Tags: %s \n' % ','.join(note_tags)
        md_note += 'Authors: %s \n' % note.attributes.author
        md_note += 'Summary: %s \n' % note_store.getNoteSearchText(self.client.token, note.guid, True, False)
        try:
            # those magic numbers(74,11) are used to cut out evernote specific markup
            md_note += '\n' + md(note.content.decode('utf-8')[74:-11:])
        except Exception:
            # get just text in case of failure to md the content
            md_note += note_store.getNoteSearchText(self.client.token, note.guid, True, False)
        return md_note

    def _note_exist(self, guid):
        return os.path.isfile(self.get_evernote_article_path() + self.evernote_note_prefix + guid + '.md')

    def get_evernote_article_path(self):
        path = self.settings['PATH'] + '/'
        if self.evernote_article_folder in self.settings.keys():
            path += self.settings[self.evernote_article_folder] + '/'
            if not os.path.isdir(path):
                raise UserWarning('%s folder does not exist!' % path)
        return path

    def _generate_notes_list(self):
        # that function is a generator for lists[10] of notes
        note_store = self.client.get_note_store()
        notes_returned = 0

        def get_note_info(offset, limit=10):
            return note_store.findNotesMetadata(self.client.token, self._get_notes_filter(), offset, limit,
                                                self._get_notes_spec())

        notes_list = []
        note_info = get_note_info(notes_returned)
        while notes_returned < int(note_info.totalNotes):
            for note in note_info.notes:
                # skip existing notes
                notes_returned += 1
                if self._note_exist(note.guid):
                    continue
                notes_list.append((note.guid, self._turn_note_into_article(note.guid, note_store)))
                if notes_returned % 10 == 0:
                    yield notes_list
                    notes_list = []
            note_info = get_note_info(notes_returned)
        yield notes_list

    @staticmethod
    def _get_notes_spec():
        # that is static for now, we are getting all the data
        spec = NotesMetadataResultSpec()
        spec.includeTitle = True
        spec.includeAttributes = True
        spec.includeCreated = True
        return spec

    def _get_notes_filter(self):
        notes_filter = NoteFilter()
        if self.filter_words in self.settings.keys():
            notes_filter.words = self.settings[self.filter_words]
        return notes_filter

    def _init_client(self, key, secret, token):
        self.client = EvernoteClient(consumer_key=key, consumer_secret=secret, token=token)


def initialize(generator):
    try:
        evernote_writer = EvernoteNotes(generator.settings)
        evernote_writer.write_all_articles()
    except (TException, UserWarning, EDAMUserException) as warning:
        logger.error('Error from evernote plugin: ' + str(warning))


def register():
    signals.article_generator_finalized.connect(initialize)
