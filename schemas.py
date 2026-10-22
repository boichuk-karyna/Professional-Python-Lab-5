from pydantic import BaseModel, ConfigDict, Field, field_validator


class AuthorCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    biography: str | None = Field(default=None, max_length=1000)

    @field_validator("name")
    @classmethod
    def clean_name(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 2:
            raise ValueError("Author name must contain at least 2 non-space characters")
        return value


class AuthorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    biography: str | None = None


class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    author_name: str = Field(min_length=2, max_length=120)
    year: int = Field(ge=1, le=2100)
    pages: int = Field(gt=0, le=100000)
    isbn: str | None = Field(default=None, min_length=10, max_length=20)

    @field_validator("title", "author_name")
    @classmethod
    def strip_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Value must not be empty")
        return value


class BookPatch(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    author_name: str | None = Field(default=None, min_length=2, max_length=120)
    year: int | None = Field(default=None, ge=1, le=2100)
    pages: int | None = Field(default=None, gt=0, le=100000)
    isbn: str | None = Field(default=None, min_length=10, max_length=20)

    @field_validator("title", "author_name")
    @classmethod
    def strip_optional_text(cls, value: str | None) -> str | None:
        if value is None:
            return value
        value = value.strip()
        if not value:
            raise ValueError("Value must not be empty")
        return value


class BookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    year: int
    pages: int
    isbn: str | None
    author_id: int
    author_name: str


class BookListResponse(BaseModel):
    items: list[BookResponse]
    total: int
    page: int
    page_size: int


class BookStatistics(BaseModel):
    total_books: int
    average_pages: float
    largest_book: BookResponse | None


class BatchAuthorsRequest(BaseModel):
    author_ids: list[int] = Field(min_length=1, max_length=20)

    @field_validator("author_ids")
    @classmethod
    def positive_ids(cls, value: list[int]) -> list[int]:
        if any(author_id <= 0 for author_id in value):
            raise ValueError("Author IDs must be positive")
        if len(set(value)) != len(value):
            raise ValueError("Author IDs must be unique")
        return value
