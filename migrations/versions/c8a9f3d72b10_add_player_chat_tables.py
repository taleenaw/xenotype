"""Add player chat tables

Revision ID: c8a9f3d72b10
Revises: ba380d281ff0
Create Date: 2026-05-07 00:05:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8a9f3d72b10'
down_revision = 'ba380d281ff0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'chat_room',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=80), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('is_public', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    op.create_table(
        'chat_message',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('room_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('body', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['room_id'], ['chat_room.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('chat_message')
    op.drop_table('chat_room')
