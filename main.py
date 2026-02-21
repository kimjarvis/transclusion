from transclude.operations.uppercase import Uppercase
from transclude.operations.include import Include
from transclude.transclude import Transclude

def main():
    t = Transclude()
    t.register("Uppercase", Uppercase)
    t.register("Include", Include)
    c, x = t.render("""

# {{ "type": "Include", "source": "example.txt", "head": 2, "tail": 2 }}
```python
```
# {{ }}    
 
    """)
    print(x)


if __name__ == "__main__":
    main()
