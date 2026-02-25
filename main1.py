from syncspec.directives.uppercase import Uppercase
from syncspec.directives.include import Include
from syncspec.directives.source import Source
from syncspec.syncspec import Syncspec

def main():
    t = Syncspec()
    t.register("Include", Include)
    t.register("Source", Source)
    c, x = t.render('''
def fib(n):
    """Return the nth Fibonacci number.

    :param int n: Index
    :rtype: int

    # {{ "type": "Include", "key": "example" }}
    assert fib(6) == 8 
    # {{ }} 
    """
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

# {{ "type": "Source", "key": "example", "head": 2 }}
def test_fib():
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
