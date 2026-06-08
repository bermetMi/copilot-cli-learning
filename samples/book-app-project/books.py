import json
from dataclasses import dataclass, asdict
from typing import List, Optional
from contextlib import contextmanager
from pathlib import Path
from exceptions import (
    CorruptedDataError,
    DataFileNotFoundError,
    InvalidYearRangeError,
    EmptyTitleError,
)

DATA_FILE = "data.json"


@contextmanager
def open_book_data(filepath: str, mode: str = 'r'):
    """Context manager for safely opening the book data file.
    
    Handles file operations with proper resource cleanup and error handling.
    
    Args:
        filepath (str): Path to the data file.
        mode (str): File open mode ('r' for read, 'w' for write).
    
    Yields:
        File object for reading or writing.
    
    Raises:
        CorruptedDataError: If reading and JSON is invalid.
        FileNotFoundError: If reading and file doesn't exist.
        IOError: If write operations fail.
    
    Examples:
        >>> with open_book_data('data.json', 'r') as f:
        ...     data = json.load(f)
    """
    file_handle = None
    try:
        file_handle = open(filepath, mode, encoding='utf-8')
        yield file_handle
    finally:
        if file_handle is not None:
            file_handle.close()


@dataclass
class Book:
    """Represents a book in the collection.
    
    Attributes:
        title (str): The title of the book.
        author (str): The author's name.
        year (int): Publication year (0 if unknown).
        read (bool): Whether the book has been read. Defaults to False.
    
    Examples:
        >>> book = Book("1984", "George Orwell", 1949)
        >>> book.title
        '1984'
        >>> book.read
        False
        >>> book.read = True
    """
    title: str
    author: str
    year: int
    read: bool = False


class BookCollection:
    """Manages a collection of books with persistence to JSON.
    
    The BookCollection class provides methods to add, remove, search, and
    organize books. All changes are automatically persisted to a JSON file.
    
    Attributes:
        books (List[Book]): The list of books in the collection.
    
    Examples:
        >>> collection = BookCollection()
        >>> collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
        >>> len(collection.list_books())
        1
    """
    
    def __init__(self):
        """Initialize a new BookCollection.
        
        Loads existing books from the data file if available. If the file
        doesn't exist, starts with an empty collection.
        
        Raises:
            CorruptedDataError: If the data file exists but contains invalid JSON.
        
        Examples:
            >>> collection = BookCollection()
            >>> isinstance(collection.books, list)
            True
        """
        self.books: List[Book] = []
        self.load_books()

    def load_books(self) -> None:
        """Load books from the JSON data file.
        
        Attempts to read books from the configured data file (data.json).
        If the file doesn't exist, initializes an empty collection.
        If the file is corrupted, raises an exception.
        
        Raises:
            CorruptedDataError: If the data file exists but contains invalid JSON
                or data that cannot be parsed into Book objects.
        
        Examples:
            >>> collection = BookCollection()
            >>> collection.load_books()  # Reloads from file
        
        Note:
            This method is called automatically during initialization.
            Call it manually only if you need to reload from disk.
            Uses context manager for safe file handling.
        """
        try:
            with open_book_data(DATA_FILE, 'r') as f:
                data = json.load(f)
                self.books = [Book(**b) for b in data]
        except FileNotFoundError:
            # This is expected on first run - start with empty collection
            self.books = []
        except json.JSONDecodeError as e:
            raise CorruptedDataError(DATA_FILE, e)

    def save_books(self) -> None:
        """Persist the current book collection to the JSON data file.
        
        Serializes all books to JSON format with indentation for readability
        and writes them to the configured data file.
        
        Raises:
            IOError: If unable to write to the data file due to permissions
                or disk space issues.
        
        Examples:
            >>> collection = BookCollection()
            >>> collection.books.append(Book("Test", "Author", 2020))
            >>> collection.save_books()  # Writes to data.json
        
        Note:
            This method is called automatically by add_book, remove_book,
            and mark_as_read. Manual calls are only needed for direct
            modifications to the books list.
            Uses context manager for safe file handling.
        """
        with open_book_data(DATA_FILE, 'w') as f:
            json.dump([asdict(b) for b in self.books], f, indent=2)

    def add_book(self, title: str, author: str, year: int) -> Book:
        """Add a new book to the collection and save to disk.
        
        Creates a new Book instance with the provided details, adds it to
        the collection, and immediately persists the change to disk.
        
        Args:
            title (str): The book's title. Must not be empty or whitespace-only.
            author (str): The author's name. Can be any string.
            year (int): Publication year. Use 0 for unknown publication dates.
        
        Returns:
            Book: The newly created Book object with read status set to False.
        
        Raises:
            EmptyTitleError: If title is empty, None, or contains only whitespace.
        
        Examples:
            >>> collection = BookCollection()
            >>> book = collection.add_book("1984", "George Orwell", 1949)
            >>> book.title
            '1984'
            >>> book.read
            False
            
            >>> # Adding a book with unknown year
            >>> book = collection.add_book("Unknown Date", "Author", 0)
            >>> book.year
            0
        
        Note:
            Duplicate books are allowed. The collection does not enforce
            uniqueness of titles.
        """
        if not title or not title.strip():
            raise EmptyTitleError()
        
        book = Book(title=title, author=author, year=year)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self) -> List[Book]:
        """Return all books in the collection.
        
        Returns:
            List[Book]: A list of all Book objects in the collection.
                Returns an empty list if the collection is empty.
        
        Examples:
            >>> collection = BookCollection()
            >>> collection.add_book("Book 1", "Author A", 2020)
            >>> collection.add_book("Book 2", "Author B", 2021)
            >>> books = collection.list_books()
            >>> len(books)
            2
            >>> books[0].title
            'Book 1'
        
        Note:
            Returns the actual list reference, not a copy. Modifications
            to the list will affect the collection, but won't be persisted
            unless save_books() is called.
        """
        return self.books

    def find_book_by_title(self, title: str) -> Optional[Book]:
        """Find a book by its title (case-insensitive).
        
        Searches the collection for a book whose title matches the provided
        title string. The search is case-insensitive.
        
        Args:
            title (str): The title to search for. Search is case-insensitive.
        
        Returns:
            Optional[Book]: The first Book object with matching title, or None
                if no matching book is found.
        
        Examples:
            >>> collection = BookCollection()
            >>> collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
            >>> book = collection.find_book_by_title("the hobbit")
            >>> book is not None
            True
            >>> book.title
            'The Hobbit'
            
            >>> not_found = collection.find_book_by_title("Nonexistent Book")
            >>> not_found is None
            True
        
        Note:
            If multiple books have the same title, only the first match
            is returned. The search order is the order books were added.
        """
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def mark_as_read(self, title: str) -> bool:
        """Mark a book as read by its title and persist the change.
        
        Searches for a book by title (case-insensitive) and sets its read
        status to True. The change is immediately saved to disk.
        
        Args:
            title (str): The title of the book to mark as read. Search is
                case-insensitive.
        
        Returns:
            bool: True if the book was found and marked as read, False if
                the book was not found in the collection.
        
        Examples:
            >>> collection = BookCollection()
            >>> collection.add_book("1984", "George Orwell", 1949)
            >>> success = collection.mark_as_read("1984")
            >>> success
            True
            >>> book = collection.find_book_by_title("1984")
            >>> book.read
            True
            
            >>> # Try to mark non-existent book
            >>> success = collection.mark_as_read("Nonexistent")
            >>> success
            False
        
        Note:
            If a book is already marked as read, calling this method again
            has no effect but still returns True and saves to disk.
        """
        book = self.find_book_by_title(title)
        if book:
            book.read = True
            self.save_books()
            return True
        return False

    def remove_book(self, title: str) -> bool:
        """Remove a book from the collection by its title.
        
        Searches for a book by title (case-insensitive) and removes it from
        the collection. The change is immediately persisted to disk.
        
        Args:
            title (str): The title of the book to remove. Search is
                case-insensitive.
        
        Returns:
            bool: True if the book was found and removed, False if the book
                was not found in the collection.
        
        Examples:
            >>> collection = BookCollection()
            >>> collection.add_book("To Delete", "Author", 2020)
            >>> len(collection.list_books())
            1
            >>> success = collection.remove_book("To Delete")
            >>> success
            True
            >>> len(collection.list_books())
            0
            
            >>> # Try to remove non-existent book
            >>> success = collection.remove_book("Not Here")
            >>> success
            False
        
        Note:
            If multiple books have the same title, only the first match
            is removed. To remove all duplicates, call this method repeatedly
            until it returns False.
        """
        book = self.find_book_by_title(title)
        if book:
            self.books.remove(book)
            self.save_books()
            return True
        return False

    def find_by_author(self, author: str) -> List[Book]:
        """Find all books by a specific author (case-insensitive).
        
        Searches the collection for all books written by the specified author.
        The search is case-insensitive and matches exact author names only.
        
        Args:
            author (str): The author's name to search for. Search is
                case-insensitive but must match the full author name.
        
        Returns:
            List[Book]: A list of all Book objects by the specified author.
                Returns an empty list if no books by that author are found.
        
        Examples:
            >>> collection = BookCollection()
            >>> collection.add_book("1984", "George Orwell", 1949)
            >>> collection.add_book("Animal Farm", "George Orwell", 1945)
            >>> collection.add_book("Brave New World", "Aldous Huxley", 1932)
            >>> orwell_books = collection.find_by_author("george orwell")
            >>> len(orwell_books)
            2
            >>> orwell_books[0].title
            '1984'
            
            >>> # Search for author not in collection
            >>> books = collection.find_by_author("Unknown Author")
            >>> len(books)
            0
        
        Note:
            The search matches the entire author field. Partial matches
            (e.g., "Orwell" instead of "George Orwell") will not be found.
        """
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
            InvalidYearRangeError: If start > end when both are provided.

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
            raise InvalidYearRangeError(start, end)

        # Filter books (exclude year=0 as "unknown")
        return [
            b for b in self.books
            if b.year != 0
            and (start is None or b.year >= start)
            and (end is None or b.year <= end)
        ]

    def get_statistics(self) -> dict:
        """Calculate and return statistics about the book collection.
        
        Returns:
            dict: A dictionary containing:
                - total (int): Total number of books in the collection
                - read (int): Number of books marked as read
                - unread (int): Number of books not yet read
                - oldest (Optional[Book]): Book with earliest publication year,
                  or None if collection is empty or all books have year=0
                - newest (Optional[Book]): Book with latest publication year,
                  or None if collection is empty or all books have year=0
        
        Examples:
            >>> collection = BookCollection()
            >>> collection.add_book("Old Book", "Author", 1900)
            >>> collection.add_book("New Book", "Author", 2020)
            >>> collection.mark_as_read("Old Book")
            >>> stats = collection.get_statistics()
            >>> stats['total']
            2
            >>> stats['read']
            1
            >>> stats['unread']
            1
            >>> stats['oldest'].title
            'Old Book'
            >>> stats['newest'].title
            'New Book'
        
        Note:
            This method delegates to the module-level get_statistics() function.
            Books with year=0 (unknown publication date) are excluded from
            oldest/newest calculations.
        """
        return get_statistics(self.books)


def get_statistics(books: List[Book]) -> dict:
    """Calculate statistics for a list of books.
    
    This is a standalone utility function that can compute statistics
    for any list of Book objects, not just those in a BookCollection.
    
    Args:
        books (List[Book]): A list of Book objects to analyze.
    
    Returns:
        dict: A dictionary containing:
            - total (int): Total number of books in the list
            - read (int): Number of books with read=True
            - unread (int): Number of books with read=False
            - oldest (Optional[Book]): Book with smallest non-zero year,
              or None if list is empty or all books have year=0
            - newest (Optional[Book]): Book with largest non-zero year,
              or None if list is empty or all books have year=0
    
    Examples:
        >>> books = [
        ...     Book("1984", "Orwell", 1949, read=True),
        ...     Book("Dune", "Herbert", 1965, read=False),
        ...     Book("Unknown", "Author", 0, read=False)
        ... ]
        >>> stats = get_statistics(books)
        >>> stats['total']
        3
        >>> stats['read']
        1
        >>> stats['unread']
        2
        >>> stats['oldest'].title
        '1984'
        >>> stats['newest'].title
        'Dune'
        
        >>> # Empty list
        >>> stats = get_statistics([])
        >>> stats['total']
        0
        >>> stats['oldest'] is None
        True
    
    Note:
        Books with year=0 are counted in total/read/unread but excluded
        from oldest/newest determination. This treats year=0 as "unknown
        publication date" rather than "published in year 0".
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
