"""empty message

Revision ID: a7642d8ec071
Revises: fb6e7286d572
Create Date: 2016-01-22 14:47:24.116422

"""

# revision identifiers, used by Alembic.
revision = 'a7642d8ec071'
down_revision = 'fb6e7286d572'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('managementcardtype',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('m_type', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('managementcardtype')
    ### end Alembic commands ###
