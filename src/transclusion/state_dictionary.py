import json

class _ValidatedDict(dict):
    def _check(self, v):
        try:
            json.dumps(v)
        except TypeError:
            raise ValueError("Not JSON serializable")

    def __setitem__(self, k, v):
        self._check(v)
        super().__setitem__(k, v)

    def setdefault(self, k, default=None):
        self._check(default)
        return super().setdefault(k, default)

    def update(self, other=(), **kwargs):
        for v in dict(other, **kwargs).values():
            self._check(v)
        super().update(other, **kwargs)

class State_dictionary:
    def __init__(self):
        self._state = _ValidatedDict()

    @property
    def state(self):
        return self._state

    def dumps(self):
        return json.dumps(self._state)

    def loads(self, s):
        self._state.clear()
        self._state.update(json.loads(s))