from src.transclusion.filters import Uppercase, Begin, End, Include
from src.transclusion.transclude import Transclude

def main():
    t = Transclude()
    t.register("Uppercase", Uppercase)
    t.register("Begin", Begin)
    t.register("End", End)
    t.register("Include", Include)
    c, x = t.render("""

    {{ "type": "Uppercase" }}r
    abcdefg
    {{ }}r    

    {{ "type": "Include", "source": "README.md" }}r
    abcdefg
    {{ }}r    

   
    """)
    print(x)


if __name__ == "__main__":
    main()
