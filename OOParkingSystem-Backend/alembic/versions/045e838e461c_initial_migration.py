"""Initial migration

Revision ID: 045e838e461c
Revises:
Create Date: 2023-07-18 00:31:59.950448

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "045e838e461c"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "car",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("exit_time", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_car_id"), "car", ["id"], unique=False)
    op.create_table(
        "entry_point",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_entry_point_id"), "entry_point", ["id"], unique=False)
    op.create_table(
        "parking_slot",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("size", sa.String(length=2), nullable=True),
        sa.Column("car_id", sa.String(), nullable=True),
        sa.Column("start_time_occupied", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["car_id"],
            ["car.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_parking_slot_car_id"), "parking_slot", ["car_id"], unique=False
    )
    op.create_index(op.f("ix_parking_slot_id"), "parking_slot", ["id"], unique=False)
    op.create_index(
        op.f("ix_parking_slot_size"), "parking_slot", ["size"], unique=False
    )
    op.create_table(
        "parking_slot_entry_point",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("slot_id", sa.Integer(), nullable=True),
        sa.Column("entry_id", sa.Integer(), nullable=True),
        sa.Column("distance", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["entry_id"],
            ["entry_point.id"],
        ),
        sa.ForeignKeyConstraint(
            ["slot_id"],
            ["parking_slot.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_parking_slot_entry_point_distance"),
        "parking_slot_entry_point",
        ["distance"],
        unique=False,
    )
    op.create_index(
        op.f("ix_parking_slot_entry_point_entry_id"),
        "parking_slot_entry_point",
        ["entry_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_parking_slot_entry_point_id"),
        "parking_slot_entry_point",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_parking_slot_entry_point_slot_id"),
        "parking_slot_entry_point",
        ["slot_id"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_parking_slot_entry_point_slot_id"),
        table_name="parking_slot_entry_point",
    )
    op.drop_index(
        op.f("ix_parking_slot_entry_point_id"), table_name="parking_slot_entry_point"
    )
    op.drop_index(
        op.f("ix_parking_slot_entry_point_entry_id"),
        table_name="parking_slot_entry_point",
    )
    op.drop_index(
        op.f("ix_parking_slot_entry_point_distance"),
        table_name="parking_slot_entry_point",
    )
    op.drop_table("parking_slot_entry_point")
    op.drop_index(op.f("ix_parking_slot_size"), table_name="parking_slot")
    op.drop_index(op.f("ix_parking_slot_id"), table_name="parking_slot")
    op.drop_index(op.f("ix_parking_slot_car_id"), table_name="parking_slot")
    op.drop_table("parking_slot")
    op.drop_index(op.f("ix_entry_point_id"), table_name="entry_point")
    op.drop_table("entry_point")
    op.drop_index(op.f("ix_car_id"), table_name="car")
    op.drop_table("car")
    # ### end Alembic commands ###
