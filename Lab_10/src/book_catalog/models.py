from dataclasses import dataclass
from typing import Optional

@dataclass
class Author:
    id: int
    name: str
    country: str = "Unknown"

@dataclass
class Book:
    id: int
    title: str
    author_id: int
    year: int
    genre: str
    isbn: Optional[str] = None
    price: float = 0.0
