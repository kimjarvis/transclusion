
# Example

```python
def fib(n):
    """Return the nth Fibonacci number.

    :param int n: Index
    :rtype: int

    assert fib(6) == 8
    """
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

def test_fib():
    assert fib(6) == 8
```



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

def test_fib():
    # {{ "type": "Source", "key": "example" }}
    assert fib(6) == 8 
    # {{ }}    
```

The fragment wrapped by the `Source` directive is used to update the target, marked by the `Include` directive, in the docstring. 
The update is idempotent.  
If the unit test is modified to, for example, `assert fib(9) == 34` the docstring is updated.

The unit test is the source of truth and the example in the docstring is a live copy.  This is preferred over using the example as the source of truth as 
the unit test is a refactoring target.  It should be noted that  
python has a builtin tool, doctest, to keep docstrings in sync with code.  It works the other way around, the docstring is the source of truth.

