from process_chunks import process_chunks


def main():
    print("Transclusion")

    x = process_chunks([[
        """
            {  "name": "John Doe" } 
        """,
        "B",
        """
            {  "title": "John Doe" }
        """]])

    print(x)


if __name__ == "__main__":
    main()
