from typing import Tuple, Iterable, Any, Protocol, Optional
from exceptions import (
    InvalidMenuChoiceError,
    TooManyAttemptsError,
    InputInterruptedError,
    EmptyTitleError,
    InvalidYearError,
)


class BookLike(Protocol):
    """Protocol describing the minimal book attributes used by utilities."""

    title: str
    author: str
    year: int
    read: bool


# ============================================================================
# DATA VALIDATION & PROCESSING FUNCTIONS (Pure Logic, No Display)
# ============================================================================

def validate_menu_choice(choice: str, valid_choices: set[str]) -> Optional[str]:
    """Validate a menu choice input.
    
    Args:
        choice: The user's input string.
        valid_choices: Set of valid choice strings.
    
    Returns:
        Error message if invalid, None if valid.
    """
    if not choice:
        return "Input cannot be empty. Please enter a number between 1 and 5."
    
    if not choice.isdigit():
        return f"'{choice}' is not a valid number. Please enter a number between 1 and 5."
    
    if choice not in valid_choices:
        return f"'{choice}' is out of range. Please enter a number between 1 and 5."
    
    return None


def parse_year_input(year_input: str) -> int:
    """Parse and validate year input.
    
    Args:
        year_input: The year string from user input.
    
    Returns:
        Parsed year value (0 if empty).
    
    Raises:
        InvalidYearError: If year_input cannot be converted to integer.
    """
    if year_input == "":
        return 0
    
    try:
        year = int(year_input)
        return year
    except ValueError:
        raise InvalidYearError(year_input)


def format_book_display(book: BookLike, index: int) -> str:
    """Format a single book for display.
    
    Args:
        book: The book object to format.
        index: The index number for display.
    
    Returns:
        Formatted string representation of the book.
    """
    try:
        title = getattr(book, "title", "Untitled")
        author = getattr(book, "author", "Unknown")
        year = getattr(book, "year", 0)
        read = getattr(book, "read", False)
        status = "✅ Read" if bool(read) else "📖 Unread"
        return f"{index}. {title} by {author} ({year}) - {status}"
    except Exception as exc:
        return f"{index}. <error reading book: {exc}>"


# ============================================================================
# DISPLAY FUNCTIONS (Pure Display, No Business Logic)
# ============================================================================


def print_menu() -> None:
    """Print the main menu."""
    print("\n📚 Book Collection App")
    print("1. Add a book")
    print("2. List books")
    print("3. Mark book as read")
    print("4. Remove a book")
    print("5. Exit")


def get_user_choice() -> str:
    """Prompt the user for a menu choice and validate it.

    Returns:
        A string in {'1','2','3','4','5'} representing the selected option.

    Raises:
        InputInterruptedError: if input is interrupted (EOF/KeyboardInterrupt).
        TooManyAttemptsError: if too many invalid attempts are made.
    """
    valid_choices = {"1", "2", "3", "4", "5"}
    max_attempts = 3

    try:
        for attempt in range(1, max_attempts + 1):
            choice = input("Choose an option (1-5): ").strip()

            error = validate_menu_choice(choice, valid_choices)
            if error:
                print(error)
                continue

            return choice

        raise TooManyAttemptsError("menu choice", max_attempts)
    except (EOFError, KeyboardInterrupt):
        raise InputInterruptedError("menu choice")


def get_book_details() -> Tuple[str, str, int]:
    """Interactively prompt the user for book details via stdin.

    This function collects three pieces of information about a book through
    sequential input prompts. It includes validation and sensible defaults
    to ensure usable data is always returned.

    Input Behavior:
        - **Title** (required): The user is prompted up to 3 times if they
          provide an empty string. After 3 failed attempts, raises EmptyTitleError.
        - **Author** (optional): If left blank, defaults to ``'Unknown'``.
        - **Year** (optional): If left blank, defaults to ``0``. Invalid input
          defaults to 0 with a warning.

    Returns:
        Tuple[str, str, int]: A 3-tuple containing:
            - title (str): The book's title (guaranteed non-empty).
            - author (str): The book's author (``'Unknown'`` if not provided).
            - year (int): The publication year (``0`` if unknown).

    Raises:
        EmptyTitleError: If the user fails to provide a non-empty title after
            the maximum number of attempts (3).
        InputInterruptedError: If input is interrupted by the user (e.g., Ctrl+C
            or Ctrl+D / EOF).

    Example:
        >>> title, author, year = get_book_details()
        Enter book title: The Hobbit
        Enter author (leave blank for 'Unknown'): J.R.R. Tolkien
        Enter publication year (leave blank if unknown): 1937
        >>> print(title, author, year)
        The Hobbit J.R.R. Tolkien 1937
    """
    max_attempts = 3

    try:
        # Title is required - re-prompt if empty
        title = ""
        for _ in range(max_attempts):
            title = input("Enter book title: ").strip()
            if title:
                break
            print("Title cannot be empty. Please enter a title.")
        if not title:
            raise EmptyTitleError()

        # Author is optional - default to 'Unknown'
        author = input("Enter author (leave blank for 'Unknown'): ").strip()
        if not author:
            author = "Unknown"

        year_input = input("Enter publication year (leave blank if unknown): ").strip()
        try:
            year = parse_year_input(year_input)
        except InvalidYearError:
            print("Invalid year. Defaulting to 0.")
            year = 0

        return title, author, year
    except (EOFError, KeyboardInterrupt):
        raise InputInterruptedError("book details entry")


def print_books(books: Iterable[BookLike]) -> None:
    """Print a list/iterable of books safely.

    Handles malformed items gracefully so the UI doesn't crash when encountering
    unexpected objects in the collection.
    """
    try:
        book_list = list(books)
    except Exception:
        print("Invalid books collection provided.")
        return

    if not book_list:
        print("No books in your collection.")
        return

    print("\nYour Books:")
    for index, book in enumerate(book_list, start=1):
        formatted = format_book_display(book, index)
        print(formatted)


def print_add_book_header() -> None:
    """Display the header for adding a new book."""
    print("\nAdd a New Book\n")


def print_book_added_success() -> None:
    """Display success message after adding a book."""
    print("\nBook added successfully.\n")


def print_error(error_message: str) -> None:
    """Display an error message."""
    print(f"\nError: {error_message}\n")


def print_remove_book_header() -> None:
    """Display the header for removing a book."""
    print("\nRemove a Book\n")


def print_book_removed() -> None:
    """Display message after attempting to remove a book."""
    print("\nBook removed if it existed.\n")


def print_find_books_header() -> None:
    """Display the header for finding books by author."""
    print("\nFind Books by Author\n")


def print_help_message() -> None:
    """Display the help message with available commands."""
    print("""
Book Collection Helper

Commands:
  list     - Show all books
  add      - Add a new book
  remove   - Remove a book by title
  find     - Find books by author
  help     - Show this help message
""")
