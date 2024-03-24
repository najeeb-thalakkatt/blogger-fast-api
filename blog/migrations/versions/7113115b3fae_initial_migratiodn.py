"""Initial migratiodn

Revision ID: 7113115b3fae
Revises: a7204753bb45
Create Date: 2024-03-24 19:45:34.780691

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7113115b3fae'
down_revision: Union[str, None] = 'a7204753bb45'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('location', sa.String(), nullable=True),
                    sa.Column('hashed_password', sa.String(), nullable=True),
                    sa.Column('email', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_location'), 'users',
                    ['location'], unique=False)
    op.create_index(op.f('ix_users_name'), 'users', ['name'], unique=False)
    op.create_table('blog_posts',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(), nullable=True),
                    sa.Column('content', sa.String(), nullable=True),
                    sa.Column('owner_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_blog_posts_content'),
                    'blog_posts', ['content'], unique=False)
    op.create_index(op.f('ix_blog_posts_id'),
                    'blog_posts', ['id'], unique=False)
    op.create_index(op.f('ix_blog_posts_title'),
                    'blog_posts', ['title'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_blog_posts_title'), table_name='blog_posts')
    op.drop_index(op.f('ix_blog_posts_id'), table_name='blog_posts')
    op.drop_index(op.f('ix_blog_posts_content'), table_name='blog_posts')
    op.drop_table('blog_posts')
    op.drop_index(op.f('ix_users_name'), table_name='users')
    op.drop_index(op.f('ix_users_location'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
