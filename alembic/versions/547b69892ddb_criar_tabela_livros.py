from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "547b69892ddb"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "livros",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("titulo", sa.String(length=100), nullable=False),
        sa.Column("autor", sa.String(length=100), nullable=False),
        sa.Column("ano", sa.Integer(), nullable=False),
        sa.Column("disponivel", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_livros_id"), "livros", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_livros_id"), table_name="livros")
    op.drop_table("livros")
