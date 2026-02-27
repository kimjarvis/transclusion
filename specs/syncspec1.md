# Add class methods 

Implement a method that reads a file and transforms it in place.  The file is transformed using render_string.  This process over-writes the file content by writing to a temporary file and then then `replace()` the original.
```python
def render_file(self, file: str) -> None
```

Implement a method that recursively traverses a directory using a  glob pattern to match files.   It calls `render_file` to transform each file in place.  
```python
def render_directory(self, path: str, patterns: list[str]= None) -> None:
```

Implement pattern matching using the python pathspec utility. 

Implement a method that when given a list of directories and transform them by calling `render_directory` .
```python
def render_paths(self, paths: list[str], patterns: list[str] = None) -> None:
```

pathspec shall perform matching on the set of file paths.

# Implement these methods

In file src/syncspec/syncspec.py

In class
```python
class Syncspec(Registry, State_dictionary):  
    def __init__(self, open_delimiter: str = "{{", close_delimiter: str = "}}"):  
        State_dictionary.__init__(self)  
        super().__init__()  
        self.open_delimiter = open_delimiter  
        self.close_delimiter = close_delimiter
```

Existing code method with signature:
```python
def render_string(self, input: str) -> tuple[bool, str]:
```
Transforms a string.  
- Ignore the returned boolean indicator.  

# Make the following assumptions

- Binary files can be ignored.
- Symlinks are either skipped or handled safely by os.replace.
- Assumed the process retains ownership/permissions after os.replace.
- Encoding:  Explicitly pass encoding='utf-8' to read_text/write_text to ensure cross-platform consistency.
- Permissions: The user has read/write permissions for all target files.
- Recursion: render_directory traverses all sub-directories indefinitely.
- The patterns apply relative to the root directory being traversed.
- pathspec and pytest-mock are available in the environment.
- When traversing directories assume that all files are included unless excluded by the pattern.
- This software will not run on windows.  Assume `os.replace` is POSIX compliant.

# Write pytests to verify the functionality

- Pytests should be in a separate file.    
- Do not use a class, each test should be a function.  
- Verify the error conditions.  
- Create concise tests using `@pytest.mark.parametrize`

# Explain the solution

Describe any logical inconsistencies in the function specification and suggest improvements.

Describe any assumptions that are not explicitly stated in the function specification.
