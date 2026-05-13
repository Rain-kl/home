"""create cms site link

Revision ID: 0001_create_cms_site_link
Revises:
Create Date: 2026-05-13
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_create_cms_site_link"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "cms_site_link",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("icon", sa.String(length=64), nullable=True),
        sa.Column("name", sa.String(length=64), nullable=True),
        sa.Column("link", sa.String(length=500), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("enabled_flag", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("create_time", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("update_time", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_sort_order", "cms_site_link", ["sort_order"])
    op.create_index("idx_enabled_flag", "cms_site_link", ["enabled_flag"])


def downgrade() -> None:
    op.drop_index("idx_enabled_flag", table_name="cms_site_link")
    op.drop_index("idx_sort_order", table_name="cms_site_link")
    op.drop_table("cms_site_link")
