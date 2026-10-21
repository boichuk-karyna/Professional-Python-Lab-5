from sqlalchemy.orm import Session
from book_catalog.models import BookModel
from book_catalog.schemas import BookCreate


class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, author: str | None = None, year: int | None = None) -> list[BookModel]:
        query = self.db.query(BookModel)
        if author:
            query = query.filter(BookModel.author.ilike(f"%{author}%"))
        if year:
            query = query.filter(BookModel.year == year)
        return query.all()

    def get_by_id(self, book_id: int) -> BookModel | None:
        return self.db.query(BookModel).filter(BookModel.id == book_id).first()

    def create(self, book_data: BookCreate) -> BookModel:
        book = BookModel(**book_data.model_dump())
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book

    def get_authors(self) -> list[dict[str, str | int]]:
        authors = self.db.query(BookModel.author).distinct().all()
        result = []
        for idx, (auth,) in enumerate(authors, start=1):
            count = self.db.query(BookModel).filter(BookModel.author == auth).count()
            result.append({"id": idx, "author": auth, "books_count": count})
        return result

    def get_books_by_author_identifier(self, author_identifier: str) -> list[BookModel]:
        if author_identifier.isdigit():
            author_id = int(author_identifier)
            authors_list = self.get_authors()
            matched = [a for a in authors_list if a["id"] == author_id]
            if matched:
                target_author = str(matched[0]["author"])
                return self.get_all(author=target_author)
        return self.get_all(author=author_identifier)

    def get_stats(self) -> dict:
        books = self.get_all()
        if not books:
            return {"total_books": 0, "average_pages": 0.0, "largest_book": None}
        total = len(books)
        avg_pages = float(sum(b.pages for b in books) / total)
        largest = max(books, key=lambda b: b.pages)
        return {"total_books": total, "average_pages": avg_pages, "largest_book": largest}
