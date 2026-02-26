from syncspec.directives.uppercase import Uppercase
from syncspec.directives.include import Include
from syncspec.directives.source import Source
from syncspec.syncspec import Syncspec

def main():
    t = Syncspec(open_delimiter = "{#", close_delimiter = "#}")
    t.register("Include", Include)
    t.register("Source", Source)
    t.render_directory("trial")

if __name__ == "__main__":
    main()
