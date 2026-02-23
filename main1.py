from transclude.operations.uppercase import Uppercase
from transclude.operations.include import Include
from transclude.operations.source import Source
from transclude.transclude import Transclude

def main():
    t = Transclude()
    t.register("Include", Include)
    t.register("Source", Source)
    c, x = t.render('''
def fib(n):
    """Return the nth Fibonacci number.

    :param int n: Index
    :rtype: int

    {{ "type": "Include", "key": "example", "head": 0, "tail": 0, "prefix": "\\n    >>> ", "suffix": "\\n    " }}{{ }} 
    """
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

def test_fib():
    # {{ "type": "Source", "key": "example", "head": 1, "tail": 1, "strip": "" }}
    assert fib(6) == 8 
    # {{ }}    
''')

    print(f"x:{x}")
    print(f"Changed:{c}")
    c1, y= t.render(x)
    print(f"y:{y}")
    print(f"Changed:{c1}")
    print(f"Idempotent:{x==y}")
    print(f"state: {t.state}")

if __name__ == "__main__":
    main()
