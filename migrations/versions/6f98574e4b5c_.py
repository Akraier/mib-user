"""empty message

Revision ID: 6f98574e4b5c
Revises: 
Create Date: 2021-11-29 15:10:33.280983

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f98574e4b5c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('User',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.Unicode(length=128), nullable=False),
    sa.Column('firstname', sa.Unicode(length=128), nullable=False),
    sa.Column('lastname', sa.Unicode(length=128), nullable=False),
    sa.Column('password', sa.Unicode(length=128), nullable=True),
    sa.Column('date_of_birth', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('authenticated', sa.Boolean(), nullable=True),
    sa.Column('phone', sa.Unicode(length=128), nullable=False),
    sa.Column('filter_isactive', sa.Boolean(), nullable=True),
    sa.Column('n_report', sa.Integer(), nullable=True),
    sa.Column('ban_expired_date', sa.DateTime(), nullable=True),
    sa.Column('lottery_ticket_number', sa.Integer(), nullable=True),
    sa.Column('lottery_points', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('blacklist',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('black_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['black_id'], ['User.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'black_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blacklist')
    op.drop_table('User')
    # ### end Alembic commands ###