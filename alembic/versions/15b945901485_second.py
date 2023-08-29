"""second

Revision ID: 15b945901485
Revises: 7cd8656e7633
Create Date: 2023-08-29 17:08:07.222313

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '15b945901485'
down_revision: Union[str, None] = '7cd8656e7633'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'registro_auditoria',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('acao', sa.String(length=100), nullable=False),
        sa.Column('detalhes', sa.Text(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('registro_auditoria')
