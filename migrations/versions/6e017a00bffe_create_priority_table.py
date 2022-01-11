"""create Priority table

Revision ID: 6e017a00bffe
Revises: da236f9f8734
Create Date: 2022-01-10 22:42:10.250275

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e017a00bffe'
down_revision = 'da236f9f8734'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('UserAdmission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_joined_time', sa.DateTime(), nullable=False),
    sa.Column('student_joined_time', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('admission_id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['admission_id'], ['Admission.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('admission_id', 'student_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('UserAdmission')
    # ### end Alembic commands ###
