import sys
from books import BookCollection
from utils import (
    print_books,
    print_add_book_header,
    print_book_added_success,
    print_error,
    print_remove_book_header,
    print_book_removed,
    print_find_books_header,
    print_help_message,
)
from exceptions import (
    BookAppError,
    CorruptedDataError,
    EmptyTitleError,
    InvalidYearError,
)


# Global collection instance
try:
    collection = BookCollection()
except CorruptedDataError as e:
    print_error(f"Failed to load book collection: {e}")
    print("Starting with an empty collection. Your corrupted data file has not been modified.")
    # Create a fresh collection without loading from file
    collection = BookCollection.__new__(BookCollection)
    collection.books = []


def handle_list():
    books = collection.list_books()
    print_books(books)


def handle_add():
    print_add_book_header()

    title = input("Title: ").strip()
    author = input("Author: ").strip()
    year_str = input("Year: ").strip()

    try:
        year = int(year_str) if year_str else 0
        collection.add_book(title, author, year)
        print_book_added_success()
    except (EmptyTitleError, InvalidYearError, ValueError) as e:
        print_error(str(e))


def handle_remove():
    print_remove_book_header()

    title = input("Enter the title of the book to remove: ").strip()
    collection.remove_book(title)

    print_book_removed()


def handle_find():
    print_find_books_header()

    author = input("Author name: ").strip()
    books = collection.find_by_author(author)
    print_books(books)


def show_help():
    print_help_message()


def main():
    # Dictionary dispatch pattern for command handling
    commands = {
        "list": handle_list,
        "add": handle_add,
        "remove": handle_remove,
        "find": handle_find,
        "help": show_help,
    }

    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()

    # Get the handler function from the dictionary, or None if not found
    handler = commands.get(command)
    
    try:
        if handler:
            handler()
        else:
            print_error("Unknown command.")
            show_help()
    except BookAppError as e:
        # Catch any custom exceptions that weren't handled at lower levels
        print_error(str(e))
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)


if __name__ == "__main__":
    main()
