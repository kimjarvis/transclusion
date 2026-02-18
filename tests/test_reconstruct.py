import pytest
from reconstruct import reconstruct

@pytest.mark.parametrize("inp,args,expected", [
    (["m",["a","b","c","d","e","f","g","h",True],"n"], (), (True, "m{{a}}h{{e}}n")),
    (["m",["a","b","c","d","e","f","g","h",False],"n"], (), (False, "m{{a}}h{{e}}n")),
    (["x",["a","b","c","d","e","f","g","h",True],"y"], ("<", ">"), (True, "x<a>h<e>y")),
])
def test_valid(inp, args, expected):
    assert reconstruct(inp, *args) == expected

@pytest.mark.parametrize("inp", [
    ["item", ["short"]],
    ["item", [1,"b","c","d","e","f","g","h",True]],
    ["item", ["a","b","c","d","e","f","g",1,True]],
    ["item", ["a","b","c","d",1,"f","g","h",True]],
    ["item", ["a","b","c","d","e","f","g","h","not_bool"]],
    [123],
])
def test_invalid(inp):
    with pytest.raises(ValueError):
        reconstruct(inp)