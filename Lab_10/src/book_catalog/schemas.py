from pydantic import BaseModel, ConfigDict, Field


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, description="Назва книги")
    author: str = Field(..., min_length=1, description="Автор книги")
    year: int = Field(..., gt=0, description="Рік видання")
    pages: int = Field(..., gt=0, description="Кількість сторінок")


class BookCreate(BookBase):
    pass


class BookResponse(BookBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class AuthorResponse(BaseModel):
    id: int
    author: str
    books_count: int


class CatalogStats(BaseModel):
    total_books: int
    average_pages: float
    largest_book: BookResponse | None = None
