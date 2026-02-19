from ensure_balanced_delimiters import ensure_balanced_delimiters
from parse_delimiters import parse_delimiters
from isolate_blocks import isolate_blocks
from process_chunks import process_chunks
from validate_chunks import ChunkValidator
from execute import execute
from reconstruct import reconstruct
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
        chunks = process_chunks(blocks)
        validated = self.validate_chunks(chunks)
        executed = execute(validated)
        return reconstruct(executed, self.open_delimiter, self.close_delimiter)