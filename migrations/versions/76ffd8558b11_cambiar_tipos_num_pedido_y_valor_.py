"""cambiar tipos num_pedido y valor_volumetrico

Revision ID: 76ffd8558b11
Revises: 8f1a5aea0c7b
Create Date: 2026-09-11 21:06:08.447354

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "76ffd8558b11"
down_revision: str | Sequence[str] | None = "8f1a5aea0c7b"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table("pedido") as batch_op:
        batch_op.alter_column(
            "num_pedido",
            existing_type=sa.VARCHAR(),
            type_=sa.Integer(),
            existing_nullable=False,
        )

        batch_op.alter_column(
            "valor_volumetrico",
            existing_type=sa.FLOAT(),
            type_=sa.Integer(),
            existing_nullable=False,
        )


def downgrade() -> None:
    with op.batch_alter_table("pedido") as batch_op:
        batch_op.alter_column(
            "valor_volumetrico",
            existing_type=sa.Integer(),
            type_=sa.FLOAT(),
            existing_nullable=False,
        )

        batch_op.alter_column(
            "num_pedido",
            existing_type=sa.Integer(),
            type_=sa.VARCHAR(),
            existing_nullable=False,
        )
