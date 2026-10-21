"""Pydantic request and response schemas."""

from pydantic import BaseModel, ConfigDict, Field


class AuthorCreate(BaseModel):
    """Payload for creating an author."""

    name: str = Field(min_length=1, max_length=200)


class AuthorRead(BaseModel):
    """Public author representation."""

    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class BookCreate(BaseModel):
    """Payload for creating a book."""

    title: str = Field(min_length=1, max_length=250)
    author_id: int = Field(gt=0)
    year: int = Field(ge=1, le=2100)
    pages: int = Field(gt=0, le=100_000)


class BookRead(BaseModel):
    """Public book representation."""

    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    author_id: int
    year: int
    pages: int


class BookStatistics(BaseModel):
    """Aggregate book statistics."""

    count: int
    average_pages: float | None
    largest_book: BookRead | None
