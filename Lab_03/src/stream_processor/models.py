from dataclasses import dataclass


@dataclass(frozen=True)
class BookRecord:
    isbn: str
    title: str
    author: str
    year: int
    pages: int
