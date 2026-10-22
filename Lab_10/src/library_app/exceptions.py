class LibraryError(Exception):
    """Base exception for the library application."""


class BookNotFoundError(LibraryError):
    """Raised when a requested book does not exist."""


class InvalidBookDataError(LibraryError):
    """Raised when book data is invalid."""