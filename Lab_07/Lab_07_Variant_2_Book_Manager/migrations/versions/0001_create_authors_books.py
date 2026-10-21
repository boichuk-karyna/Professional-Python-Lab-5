"""Create authors and books tables without ISBN."""
from alembic import op
import sqlalchemy as sa
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "authors",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(length=150), nullable=False, unique=True),
        sa.Column("biography", sa.Text(), nullable=True),
    )
    op.create_table(
        "books",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("title", sa.String(length=250), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("pages", sa.Integer(), nullable=False),
        sa.Column("author_id", sa.Integer(), sa.ForeignKey("authors.id", ondelete="CASCADE"), nullable=False),
        sa.CheckConstraint("year >= 0 AND year <= 2100", name="ck_books_year"),
        sa.CheckConstraint("pages > 0", name="ck_books_pages"),
    )
    op.create_index("ix_books_author_id", "books", ["author_id"])

def downgrade() -> None:
    op.drop_index("ix_books_author_id", table_name="books")
    op.drop_table("books")
    op.drop_table("authors")
