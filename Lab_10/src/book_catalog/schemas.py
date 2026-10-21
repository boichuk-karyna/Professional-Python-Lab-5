"""Pydantic request and response schemas."""

from pydantic import BaseModel, ConfigDict, Field


class BookCreate(BaseModel):
    """Fields required to add a book."""

    title: str = Field(min_length=1, max_length=250)
    author: str = Field(min_length=1, max_length=200)
    year: int = Field(ge=0, le=2100)
    pages: int = Field(gt=0)


class BookRead(BaseModel):
    """Book response representation."""

    id: int
    title: str
    author: str
    year: int
    pages: int

    model_config = ConfigDict(from_attributes=True)


class AuthorRead(BaseModel):
    """Author response representation."""

    id: int
    name: str
    book_count: int
