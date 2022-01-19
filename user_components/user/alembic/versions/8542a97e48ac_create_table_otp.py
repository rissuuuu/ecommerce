"""create table otp

Revision ID: 8542a97e48ac
Revises: 6372f9cfc45e
Create Date: 2022-01-17 12:55:34.544168

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "8542a97e48ac"
down_revision = "6372f9cfc45e"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "ecom_otp",
        sa.Column("id", postgresql.UUID(as_uuid=False)),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("otp", sa.String(10), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), default=sa.func.now()),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )


def downgrade():
    op.drop_table("ecom_otp")
