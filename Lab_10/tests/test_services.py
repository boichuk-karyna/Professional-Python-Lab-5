def test_add_and_filter_books(service):
    service.add_book(1, "The Hobbit", "J.R.R. Tolkien", 1937, 310)
    service.add_book(2, "1984", "George Orwell", 1949, 328)

    tolkien_books = service.filter_by_author("J.R.R. Tolkien")
    assert len(tolkien_books) == 1
    assert tolkien_books[0].title == "The Hobbit"

def test_statistics(service):
    service.add_book(1, "Book A", "Author A", 2020, 100)
    service.add_book(2, "Book B", "Author B", 2021, 300)

    largest = service.get_largest_book()
    assert largest.title == "Book B"
    assert service.get_average_pages() == 200.0
