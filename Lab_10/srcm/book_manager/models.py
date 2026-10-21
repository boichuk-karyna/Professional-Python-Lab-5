from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Book:
    title: str
    author: str
    year: int
    pages: int

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("Book title cannot be empty")
        if not self.author.strip():
            raise ValueError("Book author cannot be empty")
        if not 0 < self.year <= 2100:
            raise ValueError("Publication year must be between 1 and 2100")
        if self.pages <= 0:
            raise ValueError("Page count must be positive")
