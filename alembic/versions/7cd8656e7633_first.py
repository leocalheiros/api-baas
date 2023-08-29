"""first

Revision ID: 7cd8656e7633
Revises: 
Create Date: 2023-08-29 16:46:42.995972

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7cd8656e7633'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'conta',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('numero_conta', sa.String(length=20), nullable=False),
        sa.Column('saldo', sa.Float(), nullable=False),
        sa.Column('nome_proprietario', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'transacao',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tipo_transacao', sa.String(length=10), nullable=False),
        sa.Column('valor', sa.Float(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('conta_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['conta_id'], ['conta.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    pass
