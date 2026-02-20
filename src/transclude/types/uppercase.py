from ..transclude_base import TranscludeBase

class Uppercase(TranscludeBase):
    type: str

    def execute(self, data: str, state: dict) -> str:
        return data.upper()
