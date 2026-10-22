from typing import TypedDict

from library_app.models import Author, Book
from library_app.value_objects import PublicationInfo


class BookPayload(TypedDict):
    id: int
    title: str
    author_first_name: str
    author_last_name: str
    pages: int
    year: int
    publisher: str


def book_from_payload(
    data: BookPayload,
) -> Book:

    author = Author(
        id=1,
        first_name=data["author_first_name"],
        last_name=data["author_last_name"],
    )

    publication_info = PublicationInfo(
        year=data["year"],
        publisher=data["publisher"],
    )

    return Book(
        book_id=data["id"],
        title=data["title"],
        author=author,
        pages=data["pages"],
        publication_info=publication_info,
    )