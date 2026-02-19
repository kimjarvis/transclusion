from filters import Uppercase, Begin, End
from transclude import Transclude

def main():
    print("Transclusion")

    t = Transclude()
    t.register("Uppercase", Uppercase)
    t.register("Begin", Begin)
    t.register("End", End)
    c, x = t.execute("""

    {{ { "type": "Uppercase" } }}r
    abcdefg
    {{ { "type": "End" } }}r    
   
    """)
    print(x)


if __name__ == "__main__":
    main()
