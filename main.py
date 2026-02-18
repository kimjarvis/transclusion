from ensure_balanced_parentheses import ensure_balanced_parentheses
from parse_parentheses import parse_parentheses
from isolate_blocks import isolate_blocks
from process_chunks import process_chunks
from validate_chunks import validate_chunks
from execute import (execute)

import pprint

def main():
    print("Transclusion")

    input = """

    {{ { "type": "Uppercase" } }}
    abcdefg
    {{ { "type": "End" } }}    
   
    """
    ensure_balanced_parentheses(input)
    a = parse_parentheses(input)
    print(a)
    b = isolate_blocks(a)
    print(b)
    c = process_chunks(b)
    print(c)
    d = validate_chunks(c)
    print(d)
    pprint.pp(d)
    e = execute(d)
    print(e)

if __name__ == "__main__":
    main()
