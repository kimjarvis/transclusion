from ensure_balanced_parentheses import ensure_balanced_parentheses
from parse_parentheses import parse_parentheses
from isolate_blocks import isolate_blocks
from process_chunks import process_chunks
from validate_chunks import ChunkValidator
from execute import execute
from reconstruct import reconstruct
from filters import Uppercase, Begin, End


import pprint

def transclude(input: str, open_parentheses: str = "{{", close_parentheses: str = "}}") -> tuple[bool, str]:
    ensure_balanced_parentheses(input,  open_parentheses, close_parentheses)
    a = parse_parentheses(input, open_parentheses, close_parentheses)
    print(a)
    b = isolate_blocks(a)
    print(b)
    c = process_chunks(b)
    print(c)
    v = ChunkValidator()
    v.register("Uppercase", Uppercase)
    v.register("Begin", Begin)
    v.register("End", End)
    d = v.validate_chunks(c)
    print(d)
    # pprint.pp(d)
    e = execute(d)
    print(e)
    c,f = reconstruct(e, open_parentheses, close_parentheses)
    print(f)
    return c,f




def main():
    print("Transclusion")

    transclude("""

    {{ { "type": "Uppercase" } }}
    abcdefg
    {{ { "type": "End" } }}    
   
    """)



if __name__ == "__main__":
    main()
