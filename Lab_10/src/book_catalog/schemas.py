from pydantic import BaseModel, ConfigDict, Field


class AuthorCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)


class AuthorRead(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    author: str = Field(min_length=1, max_length=200)
    year: int = Field(ge=0, le=2100)
    pages: int = Field(gt=0, le=100000)


class BookRead(BaseModel):
    id: int
    title: str
    author_id: int
    author: str
    year: int
    pages: int


class BookStatistics(BaseModel):
    count: int
    average_pages: float | None
    largest_book: BookRead | None
