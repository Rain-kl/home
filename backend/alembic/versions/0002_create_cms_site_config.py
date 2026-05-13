"""create cms site config

Revision ID: 0002_create_cms_site_config
Revises: 0001_create_cms_site_link
Create Date: 2026-05-13
"""

from alembic import op
import sqlalchemy as sa

revision = "0002_create_cms_site_config"
down_revision = "0001_create_cms_site_link"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "cms_site_config",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("config_key", sa.String(length=64), nullable=False),
        sa.Column("config_value", sa.Text(), nullable=True),
        sa.Column("config_group", sa.String(length=32), nullable=False, server_default="site"),
        sa.Column("label", sa.String(length=64), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("create_time", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("update_time", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("config_key", name="uk_config_key"),
    )
    op.create_index("idx_config_group", "cms_site_config", ["config_group"])


def downgrade() -> None:
    op.drop_index("idx_config_group", table_name="cms_site_config")
    op.drop_table("cms_site_config")
