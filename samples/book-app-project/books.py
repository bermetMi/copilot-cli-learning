import json
from dataclasses import dataclass, asdict
from typing import List, Optional

DATA_FILE = "data.json"


@dataclass
class Book:
    title: str
    author: str
    year: int
    read: bool = False


class BookCollection:
    def __init__(self):
        self.books: List[Book] = []
        self.load_books()

    def load_books(self):
        """Load books from the JSON file if it exists."""
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.books = [Book(**b) for b in data]
        except FileNotFoundError:
            self.books = []
        except json.JSONDecodeError:
            print("Warning: data.json is corrupted. Starting with empty collection.")
            self.books = []

    def save_books(self):
        """Save the current book collection to JSON."""
        with open(DATA_FILE, "w") as f:
            json.dump([asdict(b) for b in self.books], f, indent=2)

    def add_book(self, title: str, author: str, year: int) -> Book:
        book = Book(title=title, author=author, year=year)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self) -> List[Book]:
        return self.books

    def find_book_by_title(self, title: str) -> Optional[Book]:
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def mark_as_read(self, title: str) -> bool:
        book = self.find_book_by_title(title)
        if book:
            book.read = True
            self.save_books()
            return True
        return False

    def remove_book(self, title: str) -> bool:
        """Remove a book by title."""
        book = self.find_book_by_title(title)
        if book:
            self.books.remove(book)
            self.save_books()
            return True
        return False

    def find_by_author(self, author: str) -> List[Book]:
        """Find all books by a given author."""
        return [b for b in self.books if b.author.lower() == author.lower()]

    def list_by_year(
        self, start: Optional[int] = None, end: Optional[int] = None
    ) -> List[Book]:
        """Return books published within a year range (inclusive).

        Filters the collection to books whose publication year falls within
        [start, end]. Supports open-ended ranges by passing None.

        Args:
            start: Minimum publication year (inclusive). If None, no lower bound.
            end: Maximum publication year (inclusive). If None, no upper bound.

        Returns:
            List[Book]: Books matching the year range. Books with year=0
                (unknown publication date) are excluded from filtered results.

        Raises:
            ValueError: If start > end when both are provided.

        Examples:
            >>> collection.list_by_year(1950, 1960)  # 1950-1960 inclusive
            >>> collection.list_by_year(None, 1960)  # up to 1960
            >>> collection.list_by_year(2000, None)  # 2000 onwards
            >>> collection.list_by_year(None, None)  # all books
        """
        # Return all books if no constraints
        if start is None and end is None:
            return self.books[:]

        # Validate range
        if start is not None and end is not None and start > end:
            raise ValueError(f"start ({start}) must be <= end ({end})")

        # Filter books (exclude year=0 as "unknown")
        return [
            b for b in self.books
            if b.year != 0
            and (start is None or b.year >= start)
            and (end is None or b.year <= end)
        ]

    def get_statistics(self) -> dict:
        """Return statistics about the book collection."""
        return get_statistics(self.books)


def get_statistics(books: List[Book]) -> dict:
    """Return statistics for a list of books.

    Returns a dict with:
      - total: total number of books
      - read: number of books marked as read
      - unread: number of books not yet read
      - oldest: Book with the smallest year (None if list is empty)
      - newest: Book with the largest year (None if list is empty)
    """
    if not books:
        return {"total": 0, "read": 0, "unread": 0, "oldest": None, "newest": None}

    read_books = [b for b in books if b.read]
    dated_books = [b for b in books if b.year]

    return {
        "total": len(books),
        "read": len(read_books),
        "unread": len(books) - len(read_books),
        "oldest": min(dated_books, key=lambda b: b.year) if dated_books else None,
        "newest": max(dated_books, key=lambda b: b.year) if dated_books else None,
    }
