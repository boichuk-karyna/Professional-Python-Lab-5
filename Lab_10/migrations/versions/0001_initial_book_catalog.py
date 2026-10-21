"""Create the initial book catalog schema."""
from alembic import op
import sqlalchemy as sa

revision = "0001_book_catalog"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "authors",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("biography", sa.String(length=1000), nullable=True),
        sa.UniqueConstraint("name", name="uq_authors_name"),
    )
    op.create_index("ix_authors_id", "authors", ["id"], unique=False)
    op.create_index("ix_authors_name", "authors", ["name"], unique=False)
    op.create_table(
        "books",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("pages", sa.Integer(), nullable=False),
        sa.Column("isbn", sa.String(length=20), nullable=True),
        sa.Column("author_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["author_id"], ["authors.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("isbn", name="uq_books_isbn"),
    )
    op.create_index("ix_books_id", "books", ["id"], unique=False)
    op.create_index("ix_books_title", "books", ["title"], unique=False)
    op.create_index("ix_books_year", "books", ["year"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_books_year", table_name="books")
    op.drop_index("ix_books_title", table_name="books")
    op.drop_index("ix_books_id", table_name="books")
    op.drop_table("books")
    op.drop_index("ix_authors_name", table_name="authors")
    op.drop_index("ix_authors_id", table_name="authors")
    op.drop_table("authors")
