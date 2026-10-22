from book_catalog.repositories import BookRepository, AuthorRepository

def test_book_repo_get_all():
    repo = BookRepository()
    books = repo.get_all()
    assert len(books) >= 2

def test_author_repo_get_all():
    repo = AuthorRepository()
    authors = repo.get_all()
    assert len(authors) >= 2
