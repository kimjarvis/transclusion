from ensure_balanced_parentheses import ensure_balanced_parentheses
from parse_parentheses import parse_parentheses
from isolate_blocks import isolate_blocks
from process_chunks import process_chunks
from validate_chunks import ChunkValidator
from execute import execute
from reconstruct import reconstruct
from filters import Uppercase, Begin, End

class Transclude(ChunkValidator):
    def __init__(self):
        self.open_parentheses = "{{"
        self.close_parentheses = "}}"
        super().__init__()

    def execute(self, input: str) -> tuple[bool, str]:
        ensure_balanced_parentheses(input, self.open_parentheses, self.close_parentheses)
        parsed = parse_parentheses(input, self.open_parentheses, self.close_parentheses)
        blocks = isolate_blocks(parsed)
        chunks = process_chunks(blocks)
        validated = self.validate_chunks(chunks)
        executed = execute(validated)
        return reconstruct(executed, self.open_parentheses, self.close_parentheses)