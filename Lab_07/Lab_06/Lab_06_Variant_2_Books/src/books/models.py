"""Domain model and validation for books."""
from dataclasses import asdict, dataclass
import math


class BookValidationError(ValueError):
    """Raised when a book record is invalid."""


@dataclass(frozen=True, slots=True)
class Book:
    title: str
    author: str
    year: int
    pages: int

    def __post_init__(self) -> None:
        if not isinstance(self.title, str) or not self.title.strip():
            raise BookValidationError("Title cannot be empty.")
        if not isinstance(self.author, str) or not self.author.strip():
            raise BookValidationError("Author cannot be empty.")
        if isinstance(self.year, bool) or not isinstance(self.year, int):
            raise BookValidationError("Year must be an integer.")
        if not 0 < self.year <= 2100:
            raise BookValidationError("Year must be between 1 and 2100.")
        if isinstance(self.pages, bool) or not isinstance(self.pages, int):
            raise BookValidationError("Pages must be an integer.")
        if self.pages <= 0:
            raise BookValidationError("Pages must be greater than zero.")

    def to_dict(self) -> dict[str, object]:
        return asdict(self)
