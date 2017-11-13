import re
import subprocess
from typing import List, Tuple

from . import util


class Keyword:
    def __init__(self, *, keyword:str, kind: str, count: int):
        self.keyword = keyword
        self.kind = kind
        self.count = count


class Exiv2Parser:
    @classmethod
    def get_exiv2_version(cls) -> Tuple[str, str]:
        commands = ['exiv2', '--version']
        process = subprocess.Popen(commands, stdout=subprocess.PIPE)
        output = util.to_str(process.communicate()[0])
        match = re.search(r'exiv2 ([\d.]+) (\w+)', output)
        if match is not None:
            return match.groups()
        return None

    @classmethod
    def get_values(cls, file_path: str) -> dict:
        keywords = cls.__get_keys(file_path)
        result = dict()
        for key in keywords:
            commands = ['exiv2', '-K', key.keyword, '-P', 't', 'print', file_path]
            process = subprocess.Popen(commands, stdout=subprocess.PIPE)
            output = util.to_str(process.communicate()[0]).rstrip('\n')
            # Check if the key is a list or scalar
            if key.count > 1:
                result[key.keyword] = output.split('\n')  # Assume the output is like keywords, one per line
            else:
                result[key.keyword] = output  # Assume the whole input is the value
        return result

    @classmethod
    def __get_keys(cls, file_path: str) -> List[Keyword]:
        found_keywords = dict()
        commands = ['exiv2', '-P', 'ky', 'print', file_path]
        process = subprocess.Popen(commands, stdout=subprocess.PIPE)
        output = util.to_str(process.communicate()[0])
        for match in re.finditer(r'([\w.]+)\W+(\w+)\W*\n?', output):
            code, kind = match.groups()
            keyword = found_keywords.get(code, Keyword(keyword=code, kind=kind, count=0))
            keyword.count += 1
            found_keywords[code] = keyword

        return list(found_keywords.values())

if __name__ == '__main__':
    #data = Exiv2Parser.get_values('content/blog/terms2.jpeg')
    #print(data)
    version_info = Exiv2Parser.get_exiv2_version()
    print(version_info)


