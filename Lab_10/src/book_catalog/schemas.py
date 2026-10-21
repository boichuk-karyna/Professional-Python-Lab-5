"""Pydantic request and response schemas."""

from pydantic import BaseModel, ConfigDict, Field


class BookCreate(BaseModel):
    """Fields required to add a book."""

    title: str = Field(min_length=1, max_length=250)
    author: str = Field(min_length=1, max_length=200)
    year: int = Field(ge=0, le=2100)
    pages: int = Field(gt=0, le=100_000)


class BookRead(BookCreate):
    """Book response including its database identifier."""

    id: int
    model_config = ConfigDict(from_attributes=True)


class BookUpdate(BaseModel):
    """Optional fields for updating a book."""

    title: str | None = Field(default=None, min_length=1, max_length=250)
    author: str | None = Field(default=None, min_length=1, max_length=200)
    year: int | None = Field(default=None, ge=0, le=2100)
    pages: int | None = Field(default=None, gt=0, le=100_000)


class CatalogStatistics(BaseModel):
    """Summary statistics for the catalog."""

    total_books: int
    average_pages: float
    largest_book: BookRead | None
