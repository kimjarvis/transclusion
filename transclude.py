from ensure_balanced_delimiters import ensure_balanced_delimiters
from parse_delimiters import parse_delimiters
from isolate_blocks import isolate_blocks
from blocks_to_dictionaries import blocks_to_dictionaries
from dictionaries_to_filters import Registry
from execute_filters import execute_filters
from reassemble_document import reassemble_document


class Transclude(Registry):
    def __init__(self, open_delimiter: str = "{{", close_delimiter: str = "}}"):
        super().__init__()
        self.open_delimiter = open_delimiter
        self.close_delimiter = close_delimiter

    def render(self, source: str) -> tuple[bool, str]:
        ensure_balanced_delimiters(source, self.open_delimiter, self.close_delimiter)
        parsed = parse_delimiters(source, self.open_delimiter, self.close_delimiter)
        blocks = isolate_blocks(parsed)
        chunks = blocks_to_dictionaries(blocks)
        validated = self.dictionaries_to_filters(chunks)
        executed = execute_filters(validated)
        return reassemble_document(executed, self.open_delimiter, self.close_delimiter)