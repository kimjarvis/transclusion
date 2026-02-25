from .ensure_balanced_delimiters import ensure_balanced_delimiters
from .parse_delimiters import parse_delimiters
from .isolate_blocks import isolate_blocks
from .blocks_to_dictionaries import blocks_to_dictionaries
from .dictionaries_to_operations import Registry
from .execute_phase_one import execute_phase_one
from .execute_phase_two import execute_phase_two
from .reassemble_document import reassemble_document
from .state_dictionary import State_dictionary


class Syncspec(Registry, State_dictionary):
    def __init__(self, open_delimiter: str = "{{", close_delimiter: str = "}}"):
        State_dictionary.__init__(self)
        super().__init__()
        self.open_delimiter = open_delimiter
        self.close_delimiter = close_delimiter

    def render(self, input: str) -> tuple[bool, str]:
        ensure_balanced_delimiters(input, self.open_delimiter, self.close_delimiter)
        parsed = parse_delimiters(input, self.open_delimiter, self.close_delimiter)
        blocks = isolate_blocks(parsed)
        chunks = blocks_to_dictionaries(blocks)
        validated = self.dictionaries_to_operations(chunks)
        phase_one = execute_phase_one(validated, self.state)
        executed = execute_phase_two(phase_one, self.state)
        return reassemble_document(executed, self.open_delimiter, self.close_delimiter)