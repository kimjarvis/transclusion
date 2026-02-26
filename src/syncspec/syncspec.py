import os
import tempfile
from pathlib import Path
from typing import List

import pathspec


from .ensure_balanced_delimiters import ensure_balanced_delimiters
from .parse_delimiters import parse_delimiters
from .isolate_blocks import isolate_blocks
from .blocks_to_dictionaries import blocks_to_dictionaries
from .dictionaries_to_directives import Registry
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

    def render_string(self, input: str) -> tuple[bool, str]:
        ensure_balanced_delimiters(input, self.open_delimiter, self.close_delimiter)
        parsed = parse_delimiters(input, self.open_delimiter, self.close_delimiter)
        blocks = isolate_blocks(parsed)
        chunks = blocks_to_dictionaries(blocks)
        validated = self.dictionaries_to_directives(chunks)
        phase_one = execute_phase_one(validated, self.state)
        executed = execute_phase_two(phase_one, self.state)
        return reassemble_document(executed, self.open_delimiter, self.close_delimiter)

    def render_file(self, file: str) -> None:
        path = Path(file)
        try:
            content = path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            return  # Ignore binary files

        _, new_content = self.render_string(content)

        fd, temp_path = tempfile.mkstemp(dir=path.parent, suffix='.tmp')
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                f.write(new_content)
            os.replace(temp_path, path)
        except Exception:
            os.unlink(temp_path)
            raise

    def render_directory(self, path: str, patterns: list[str] = None) -> None:
        root = Path(path)
        spec = pathspec.PathSpec.from_lines('gitignore', patterns) if patterns else None

        for file_path in root.rglob('*'):
            if not file_path.is_file():
                continue

            # Binary check handled in render_file, but skip early if possible
            # Pathspec matches relative to root
            rel_path = str(file_path.relative_to(root))

            # Assumption: Patterns are exclusions ("included unless excluded")
            if spec and spec.match_file(rel_path):
                continue

            self.render_file(str(file_path))

    def render_paths(self, paths: list[str], patterns: list[str] = None) -> None:
        for path in paths:
            self.render_directory(path, patterns)