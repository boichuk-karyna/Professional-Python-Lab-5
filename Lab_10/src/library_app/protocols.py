import json
from typing import Protocol, runtime_checkable

from library_app.models import Book


@runtime_checkable
class Exporter(Protocol):

    def export(
        self,
        books: list[Book],
    ) -> str:
        ...


class JsonExporter:

    def export(
        self,
        books: list[Book],
    ) -> str:

        data = [
            {
                "id": book.id,
                "title": book.title,
                "author": book.author.full_name,
                "pages": book.pages,
                "year": book.publication_info.year,
                "publisher": book.publication_info.publisher,
            }
            for book in books
        ]

        return json.dumps(
            data,
            indent=2,
            ensure_ascii=False,
        )


class ConsoleExporter:

    def export(
        self,
        books: list[Book],
    ) -> str:

        return "\n".join(
            str(book)
            for book in books
        )


class Notifier(Protocol):

    def send(
        self,
        message: str,
    ) -> None:
        ...


class ConsoleNotifier:

    def send(
        self,
        message: str,
    ) -> None:

        print(
            f"NOTIFICATION: {message}"
        )