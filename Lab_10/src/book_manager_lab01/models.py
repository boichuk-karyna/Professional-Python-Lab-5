from dataclasses import dataclass


@dataclass
class Book:
    title: str
    author: str
    year: int
    pages: int