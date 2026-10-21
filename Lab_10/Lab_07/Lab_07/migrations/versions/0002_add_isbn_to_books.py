"""Add ISBN to books."""
from alembic import op
import sqlalchemy as sa

revision = "0002_add_isbn"
down_revision = "0001_authors_books"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("books", sa.Column("isbn", sa.String(length=20), nullable=True))
    op.create_unique_constraint("uq_books_isbn", "books", ["isbn"])


def downgrade() -> None:
    op.drop_constraint("uq_books_isbn", "books", type_="unique")
    op.drop_column("books", "isbn")
