
# Example

```python
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
```

The fragment wrapped by the `Source` directive is used to update the target, marked by the `Include` directive, in the docstring. 
The update is idempotent.  
If the unit test is modified to, for example, `assert fib(9) == 34` the docstring is updated.

The `key` is used to identify a fragment.  The key is specified in the `Include` directive.  The fragment is copied into the target block.

The `head` is the number of source lines to skip when copying the fragment.  The first line contains the directive and the second line contains `test_fib`.

In this example, the unit test is the source of truth the docstring is a live copy.  
It should be noted that python has a builtin tool to keep docstrings in sync with code, called doctest, works the other way around.  
The docstring is the source of truth and unit tests are generated from it.
This can cause problems as the unit test is the refactoring target.
