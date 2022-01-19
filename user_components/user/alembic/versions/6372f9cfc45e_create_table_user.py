"""create table user

Revision ID: 6372f9cfc45e
Revises:
Create Date: 2021-06-23 14:16:39.296726

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "6372f9cfc45e"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "ecom_user",
        sa.Column("id", postgresql.UUID(as_uuid=False)),
        sa.Column("first_name", sa.String(255), nullable=False),
        sa.Column("last_name", sa.String(255), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("user_name", sa.String(255), nullable=False),
        sa.Column("password", sa.String(255)),
        sa.Column("is_active", sa.Boolean(), server_default="f", default=False),
        sa.Column("phone_number", sa.String(255)),
        sa.Column("is_admin", sa.Boolean(), server_default="f", default=False),
        sa.Column("is_customer", sa.Boolean(), server_default="f", default=False),
        sa.Column("is_seller", sa.Boolean(), server_default="f", default=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), default=sa.func.now()),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_name"),
    )


def downgrade():
    op.drop_table("ecom_user")
