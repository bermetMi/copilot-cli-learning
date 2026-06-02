from typing import Tuple, Iterable, Any, Protocol


class BookLike(Protocol):
    """Protocol describing the minimal book attributes used by utilities."""

    title: str
    author: str
    year: int
    read: bool


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
        RuntimeError: if input is interrupted (EOF/KeyboardInterrupt).
        ValueError: if too many invalid attempts are made.
    """
    valid_choices = {"1", "2", "3", "4", "5"}
    max_attempts = 3

    try:
        for attempt in range(1, max_attempts + 1):
            choice = input("Choose an option (1-5): ").strip()

            # Handle empty input
            if not choice:
                print("Input cannot be empty. Please enter a number between 1 and 5.")
                continue

            # Handle non-numeric input
            if not choice.isdigit():
                print(f"'{choice}' is not a valid number. Please enter a number between 1 and 5.")
                continue

            # Handle out-of-range numeric input
            if choice not in valid_choices:
                print(f"'{choice}' is out of range. Please enter a number between 1 and 5.")
                continue

            return choice

        raise ValueError("Too many invalid attempts for menu choice.")
    except (EOFError, KeyboardInterrupt) as exc:
        raise RuntimeError("Input aborted by user while choosing menu option.") from exc


def get_book_details() -> Tuple[str, str, int]:
    """Interactively prompt the user for book details via stdin.

    This function collects three pieces of information about a book through
    sequential input prompts. It includes validation and sensible defaults
    to ensure usable data is always returned.

    Input Behavior:
        - **Title** (required): The user is prompted up to 3 times if they
          provide an empty string. After 3 failed attempts, a ValueError
          is raised.
        - **Author** (optional): If left blank, defaults to ``'Unknown'``.
        - **Year** (optional): If left blank or non-numeric, defaults to ``0``.

    Returns:
        Tuple[str, str, int]: A 3-tuple containing:
            - title (str): The book's title (guaranteed non-empty).
            - author (str): The book's author (``'Unknown'`` if not provided).
            - year (int): The publication year (``0`` if unknown or invalid).

    Raises:
        ValueError: If the user fails to provide a non-empty title after
            the maximum number of attempts (3).
        RuntimeError: If input is interrupted by the user (e.g., Ctrl+C
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
            raise ValueError("Title is required but was not provided after multiple attempts.")

        # Author is optional - default to 'Unknown'
        author = input("Enter author (leave blank for 'Unknown'): ").strip()
        if not author:
            author = "Unknown"

        year_input = input("Enter publication year (leave blank if unknown): ").strip()
        if year_input == "":
            year = 0
        else:
            try:
                year = int(year_input)
            except ValueError:
                print("Invalid year. Defaulting to 0.")
                year = 0

        return title, author, year
    except (EOFError, KeyboardInterrupt) as exc:
        raise RuntimeError("Input aborted by user while entering book details.") from exc


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
        try:
            title = getattr(book, "title", "Untitled")
            author = getattr(book, "author", "Unknown")
            year = getattr(book, "year", 0)
            read = getattr(book, "read", False)
            status = "✅ Read" if bool(read) else "📖 Unread"
            print(f"{index}. {title} by {author} ({year}) - {status}")
        except Exception as exc:
            print(f"{index}. <error reading book: {exc}>")
            continue
