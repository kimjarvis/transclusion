def fib(n):
    """Return the nth Fibonacci number.

    :param int n: Index
    :rtype: int

    # {# "syncspec": "Include", "key": "example" #}
    assert fib(6) == 8
    # {# #}
    """
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

def test_fib():
    # {# "syncspec": "Source", "key": "example" #}
    assert fib(6) == 8
    # {# #}
