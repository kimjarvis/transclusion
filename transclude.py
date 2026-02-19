from ensure_balanced_delimiters import ensure_balanced_delimiters
from parse_delimiters import parse_delimiters
from isolate_blocks import isolate_blocks
from blocks_to_dictionaries import blocks_to_dictionaries
from dictionaries_to_filters import ChunkValidator
from execute_filters import execute_filters
from reassemble_document import reassemble_document
from filters import Uppercase, Begin, End

class Transclude(ChunkValidator):
    def __init__(self):
        self.open_delimiter = "{{"
        self.close_delimiter = "}}"
        super().__init__()

    def execute(self, input: str) -> tuple[bool, str]:
        ensure_balanced_delimiters(input, self.open_delimiter, self.close_delimiter)
        parsed = parse_delimiters(input, self.open_delimiter, self.close_delimiter)
        blocks = isolate_blocks(parsed)
        chunks = blocks_to_dictionaries(blocks)
        validated = self.dictionaries_to_filters(chunks)
        executed = execute_filters(validated)
        return reassemble_document(executed, self.open_delimiter, self.close_delimiter)