from pelican.readers import BaseReader
from pelican.generators import CachingGenerator
from pelican.contents import Page, is_valid_content
from pelican import signals
import logging
from blinker import signal
import requests
from os import listdir
from os.path import isfile, join

"""
pelican-rdf
===============

This plugin integrates to pelican a new type of media, the vocabulary.
Vocabularies are .rdf or .owl files, and metadata about them is collected
through sparql queries.
"""


try:
    import rdflib
    from rdflib.query import Processor
    rdflib_loaded=True
except ImportError:
    rdflib_loaded=False

logger = logging.getLogger(__name__)

voc_generator_init = signal('voc_generator_init')
voc_generator_finalized = signal('voc_generator_finalized')
voc_writer_finalized = signal('voc_writer_finalized')
voc_generator_preread = signal('voc_generator_preread')
voc_generator_context = signal('voc_generator_context')

class VocabularyGenerator(CachingGenerator):
    """Generate vocabulary descriptions"""

    # temporary file where the vocabulary is dereferenced to
    # when collected online
    _local_vocabulary_path = "/tmp/"
    
    def __init__(self, *args, **kwargs):
        logger.debug("Vocabulary generator called")
        self.vocabularies =[]
        super(VocabularyGenerator, self).__init__(*args, **kwargs)
    
    # Called both for local and remote vocabulary context creation.
    # Performs the actual Vocabulary generation.
    def generate_vocabulary_context(
            self, vocabulary_file_name, path_to_vocabulary):
        logger.debug("Generating__ vocabulary context for "+
            path_to_vocabulary+"/"+vocabulary_file_name)
        voc = self.get_cached_data(vocabulary_file_name, None)
        if voc is None:
            try:
                voc = self.readers.read_file(
                    base_path=path_to_vocabulary,
                    path=vocabulary_file_name,
                    content_class=Vocabulary,
                    context=self.context,
                    preread_signal=voc_generator_preread,
                    preread_sender=self,
                    context_signal=voc_generator_context,
                    context_sender=self)
            except Exception as e:
                logger.error(
                    'Could not process %s\n%s', vocabulary_file_name, e,
                    exc_info=self.settings.get('DEBUG', False))
                self._add_failed_source_path(vocabulary_file_name)
            
            if not is_valid_content(voc, vocabulary_file_name):
                self._add_failed_source_path(vocabulary_file_name)
    
            self.cache_data(vocabulary_file_name, voc)
        self.vocabularies.append(voc)
        self.add_source_path(voc)
    
    
    def generate_local_context(self):
        for f in self.get_files(
                self.settings['VOC_PATHS'],
                exclude=self.settings['VOC_EXCLUDES']):
            self.generate_vocabulary_context(f, self.path)
    
    def dereference(self, uri, local_file):
        logger.debug("Dereferencing "+uri+" into "+local_file)
        headers={"Accept":"application/rdf+xml"}
        r = requests.get(uri, headers=headers)
        with open(self._local_vocabulary_path+local_file, 'w') as f:
            f.write(r.text)
    
    def generate_remote_context(self):
        for uri in self.settings["VOC_URIS"]:
            logger.debug("Generating context for remote "+uri)
            local_name = uri.split("/")[-1]+".rdf"
            self.dereference(uri, local_name)
            self.generate_vocabulary_context(
                local_name,
                self._local_vocabulary_path)
    
    def generate_context(self):
        self.generate_local_context()
        self.generate_remote_context()
        self._update_context(('vocabularies',))
        self.save_cache()
        self.readers.save_cache()
    
    def generate_output(self, writer):
        for voc in self.vocabularies:
            writer.write_file(
                voc.save_as, self.get_template(voc.template),
                self.context, voc=voc,
                relative_urls=self.settings['RELATIVE_URLS'],
                override_output=hasattr(voc, 'override_save_as'))
        voc_writer_finalized.send(self, writer=writer)

class RdfReader(BaseReader):
    
    file_extensions = ['rdf', 'owl']
    enabled = bool(rdflib_loaded)
    
    def __init__(self, *args, **kwargs):
        super(RdfReader, self).__init__(*args, **kwargs)

    def read(self, source_path):
        """Parse content and metadata of an rdf file"""
        logger.debug("Loading graph described in "+source_path)
        graph = rdflib.Graph()
        graph.load(source_path)
        meta = {}
        queries = [
            f for f in listdir(self.settings["VOC_QUERIES_PATH"])
            if (isfile(join(self.settings["VOC_QUERIES_PATH"], f)) 
                and f.endswith(".sparql"))]
        for query_path in queries:
            query_file_path = self.settings["VOC_QUERIES_PATH"]+"/"+query_path
            with open(query_file_path, "r") as query_file:
                query = query_file.read()

                # The name of the query identifies the elements in the context
                query_key=query_path.split(".")[0]
                result_set = graph.query(query)
                # Each query result will be stored as a dictionnary in the
                # vocabulary context, referenced by the query name as its key.
                # Multiple results are stored in a list.
                for result in result_set:
                    if not query_key in meta.keys():
                        meta[query_key]=result.asdict()
                    elif type(meta[query_key]) == list:
                        meta[query_key].append(result.asdict())
                    else:
                        meta[query_key]=[meta[query_key], result.asdict()]
        meta["iri"] = meta["lov_metadata"]["iri"]
        meta["description"] = meta["lov_metadata"]["description"]
        meta["version"] = meta["lov_metadata"]["version"]
        meta["title"] = meta["lov_metadata"]["title"]
        return "", meta

class Vocabulary(Page):
    mandatory_properties = ('iri','description','version', 'title')
    default_template = 'vocabulary'

def add_reader(readers):
    for ext in RdfReader.file_extensions:
        readers.reader_classes[ext] = RdfReader

def add_generator(pelican_object):
    print("Adding the generator")
    return VocabularyGenerator


def register():
    signals.get_generators.connect(add_generator)
    signals.readers_init.connect(add_reader)
