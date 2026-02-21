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
    print(f"Changed:{c}")
    c1, y= t.render(x)
    print(y)
    print(f"Changed:{c1}")
    print(f"Idempotent:{x==y}")

if __name__ == "__main__":
    main()
