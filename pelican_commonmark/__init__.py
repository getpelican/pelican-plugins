from CommonMark import DocParser, HTMLRenderer
from pelican.readers import BaseReader, MarkdownReader
from pelican.utils import pelican_open


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


def register():
    pass
