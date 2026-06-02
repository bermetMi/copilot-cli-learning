import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books
from books import BookCollection


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch):
    """Use a temporary data file for each test."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))


def test_add_book():
    collection = BookCollection()
    initial_count = len(collection.books)
    collection.add_book("1984", "George Orwell", 1949)
    assert len(collection.books) == initial_count + 1
    book = collection.find_book_by_title("1984")
    assert book is not None
    assert book.author == "George Orwell"
    assert book.year == 1949
    assert book.read is False

def test_mark_book_as_read():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    result = collection.mark_as_read("Dune")
    assert result is True
    book = collection.find_book_by_title("Dune")
    assert book.read is True

def test_mark_book_as_read_invalid():
    collection = BookCollection()
    result = collection.mark_as_read("Nonexistent Book")
    assert result is False

def test_remove_book():
    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    result = collection.remove_book("The Hobbit")
    assert result is True
    book = collection.find_book_by_title("The Hobbit")
    assert book is None

def test_remove_book_invalid():
    collection = BookCollection()
    result = collection.remove_book("Nonexistent Book")
    assert result is False


# --- get_statistics tests ---

def test_statistics_empty_collection():
    collection = BookCollection()
    stats = collection.get_statistics()
    assert stats == {"total": 0, "read": 0, "unread": 0, "oldest": None, "newest": None}


def test_statistics_counts():
    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.mark_as_read("1984")

    stats = collection.get_statistics()
    assert stats["total"] == 3
    assert stats["read"] == 1
    assert stats["unread"] == 2


def test_statistics_oldest_and_newest():
    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("Dune", "Frank Herbert", 1965)

    stats = collection.get_statistics()
    assert stats["oldest"].title == "The Hobbit"
    assert stats["newest"].title == "Dune"


def test_statistics_standalone_function():
    from books import Book, get_statistics
    book_list = [
        Book("A", "Author1", 2000, read=True),
        Book("B", "Author2", 2010, read=False),
        Book("C", "Author3", 1990, read=True),
    ]
    stats = get_statistics(book_list)
    assert stats["total"] == 3
    assert stats["read"] == 2
    assert stats["unread"] == 1
    assert stats["oldest"].title == "C"
    assert stats["newest"].title == "B"


# --- list_by_year tests ---

def test_list_by_year_inclusive_bounds():
    """Test that both start and end years are inclusive."""
    collection = BookCollection()
    collection.add_book("Book1950", "Author", 1950)
    collection.add_book("Book1955", "Author", 1955)
    collection.add_book("Book1960", "Author", 1960)
    collection.add_book("Book1965", "Author", 1965)

    result = collection.list_by_year(1950, 1960)
    titles = [b.title for b in result]

    assert "Book1950" in titles  # start year included
    assert "Book1955" in titles
    assert "Book1960" in titles  # end year included
    assert "Book1965" not in titles


def test_list_by_year_open_start():
    """Test open-ended range with None start (up to end)."""
    collection = BookCollection()
    collection.add_book("Ancient", "Author", 1800)
    collection.add_book("Old", "Author", 1950)
    collection.add_book("Modern", "Author", 2020)

    result = collection.list_by_year(None, 1950)
    titles = [b.title for b in result]

    assert "Ancient" in titles
    assert "Old" in titles
    assert "Modern" not in titles


def test_list_by_year_open_end():
    """Test open-ended range with None end (from start onwards)."""
    collection = BookCollection()
    collection.add_book("Old", "Author", 1950)
    collection.add_book("Modern", "Author", 2000)
    collection.add_book("Recent", "Author", 2023)

    result = collection.list_by_year(2000, None)
    titles = [b.title for b in result]

    assert "Old" not in titles
    assert "Modern" in titles
    assert "Recent" in titles


def test_list_by_year_both_none_returns_all():
    """Test that None, None returns all books."""
    collection = BookCollection()
    collection.add_book("A", "Author", 1990)
    collection.add_book("B", "Author", 2000)

    result = collection.list_by_year(None, None)
    assert len(result) == 2


def test_list_by_year_empty_result():
    """Test range that matches no books."""
    collection = BookCollection()
    collection.add_book("Old", "Author", 1950)

    result = collection.list_by_year(2000, 2020)
    assert result == []


def test_list_by_year_invalid_range_raises():
    """Test that start > end raises ValueError."""
    collection = BookCollection()

    with pytest.raises(ValueError, match="start .* must be <= end"):
        collection.list_by_year(2000, 1990)


def test_list_by_year_excludes_unknown_year():
    """Test that books with year=0 are excluded from filtered results."""
    collection = BookCollection()
    collection.add_book("Known", "Author", 2000)
    collection.add_book("Unknown", "Author", 0)

    result = collection.list_by_year(1990, 2010)
    titles = [b.title for b in result]

    assert "Known" in titles
    assert "Unknown" not in titles
