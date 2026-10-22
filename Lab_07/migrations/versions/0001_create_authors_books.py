"""Create authors and books tables (before ISBN)."""
from alembic import op
import sqlalchemy as sa

revision = "0001_authors_books"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "authors",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.CheckConstraint("length(trim(name)) > 0", name="ck_authors_name_not_blank"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "books",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("title", sa.String(length=250), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("pages", sa.Integer(), nullable=False),
        sa.Column("author_id", sa.Integer(), nullable=False),
        sa.CheckConstraint("length(trim(title)) > 0", name="ck_books_title_not_blank"),
        sa.CheckConstraint("year > 0 AND year <= 2100", name="ck_books_year_range"),
        sa.CheckConstraint("pages > 0", name="ck_books_pages_positive"),
        sa.ForeignKeyConstraint(["author_id"], ["authors.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_books_author_id", "books", ["author_id"])


def downgrade() -> None:
    op.drop_index("ix_books_author_id", table_name="books")
    op.drop_table("books")
    op.drop_table("authors")
