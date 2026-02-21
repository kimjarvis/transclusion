from transclude.types.uppercase import Uppercase
from transclude.types.include import Include
from transclude.transclude import Transclude

def main():
    t = Transclude()
    t.register("Uppercase", Uppercase)
    t.register("Include", Include)
    c, x = t.render("""

# {{ "type": "Include", "source": "example.txt", "head": 2, "tail": 1 }}
```python
```
# {{ }}    
 
    """)
    print(x)


if __name__ == "__main__":
    main()
