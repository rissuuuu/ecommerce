import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

SQLMETADATA = sa.MetaData()

user = sa.Table(
    "ecom_user",
    SQLMETADATA,
    sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
    sa.Column("first_name", sa.String(255), nullable=False),
    sa.Column("last_name", sa.String(255), nullable=False),
    sa.Column("email", sa.String(255), nullable=False),
    sa.Column("user_name", sa.String(255), nullable=False),
    sa.Column("password", sa.String(255)),
    sa.Column("is_active", sa.Boolean()),
    sa.Column("phone_number", sa.String(255)),
    sa.Column("is_admin", sa.Boolean()),
    sa.Column("is_customer", sa.Boolean()),
    sa.Column("is_seller", sa.Boolean()),
    sa.Column("created_at", sa.TIMESTAMP(timezone=True), default=sa.func.now()),
    sa.Column(
        "updated_at",
        sa.TIMESTAMP(timezone=True),
        default=sa.func.now(),
        onupdate=sa.func.now(),
    ),
)
