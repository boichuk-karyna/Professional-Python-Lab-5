"""Pydantic request and response schemas."""
from pydantic import BaseModel, Field


class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=250)
    author: str = Field(min_length=1, max_length=150)
    year: int = Field(gt=0, le=3000)
    pages: int = Field(gt=0, le=100000)


class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int
    pages: int


class Author(BaseModel):
    id: int
    name: str
