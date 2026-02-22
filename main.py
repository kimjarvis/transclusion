from transclude.operations.uppercase import Uppercase
from transclude.operations.include import Include
from transclude.operations.source import Source
from transclude.transclude import Transclude

def main():
    t = Transclude()
    t.register("Uppercase", Uppercase)
    t.register("Include", Include)
    t.register("Source", Source)
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

    c, x = t.render("""
# {{ "type": "Source", "key": "example1.txt", "head": 1, "tail": 1 }}
line 1
line 2
line 3
# {{ }}    
    """)
    print(f"state: {t.state}")


if __name__ == "__main__":
    main()
