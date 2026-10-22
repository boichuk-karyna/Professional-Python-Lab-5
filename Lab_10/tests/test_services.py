from book_catalog.services import CatalogService

def test_catalog_service_list_books():
    service = CatalogService()
    books = service.list_books()
    assert len(books) > 0
