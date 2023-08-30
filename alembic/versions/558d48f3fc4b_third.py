"""third

Revision ID: 558d48f3fc4b
Revises: 15b945901485
Create Date: 2023-08-30 08:57:24.458015

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '558d48f3fc4b'
down_revision: Union[str, None] = '15b945901485'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('conta', sa.Column('cpf', sa.String(length=11), nullable=False, unique=True))
    op.add_column('conta', sa.Column('senha', sa.String(length=255), nullable=False))

def downgrade() -> None:
    op.drop_column('conta', 'cpf')
    op.drop_column('conta', 'senha')
