from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class AuthorCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)

    @field_validator("name")
    @classmethod
    def clean_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Author name cannot be empty")
        return value


class AuthorRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    author: str = Field(min_length=1, max_length=200)
    year: int = Field(ge=1450, le=2100)
    pages: int = Field(gt=0, le=100000)
    description: str | None = None

    @field_validator("title", "author")
    @classmethod
    def clean_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Value cannot be empty")
        return value


class BookRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    author_id: int
    year: int
    pages: int
    description: str | None
    created_at: datetime
    author: AuthorRead


class BookStatistics(BaseModel):
    count: int
    average_pages: float | None
    largest_book: BookRead | None
