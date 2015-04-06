from CommonMark import DocParser, HTMLRenderer
from pelican.readers import BaseReader, MarkdownReader
from pelican.utils import pelican_open
from pelican import signals


class CommonMarkReader(BaseReader):
    file_extensions = MarkdownReader.file_extensions

    def read(self, source_path):
        with pelican_open(source_path) as source:
            metadata = {}
            source_lines = []

            reading_metadata = True
            for line in source.splitlines():
                if reading_metadata:
                    if line.count(':') > 0:
                        key, value = (x.strip() for x in line.split(':', 1))
                        key = key.lower()
                        metadata[key] = self.process_metadata(key, value)
                    else:
                        reading_metadata = False
                if not reading_metadata:
                    source_lines.append(line)

            ast = DocParser().parse('\n'.join(source_lines))
            content = HTMLRenderer().render(ast)
            return content, metadata


def replace_markdown_reader(readers):
    for ext, reader in readers.reader_classes.items():
        if reader == MarkdownReader:
            readers.reader_classes[ext] = CommonMarkReader


def register():
    signals.readers_init.connect(replace_markdown_reader)
