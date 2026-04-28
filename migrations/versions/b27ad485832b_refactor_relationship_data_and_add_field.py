"""refactor relationship data and add field

Revision ID: b27ad485832b
Revises: 36746f81d920
Create Date: 2026-04-27 14:19:46.710902
"""
from alembic import op
import sqlalchemy as sa


revision = 'b27ad485832b'
down_revision = '36746f81d920'
branch_labels = None
depends_on = None


def upgrade():
    # ================================
    # 1. ADD id vào doctor_specialties TRƯỚC
    # ================================
    with op.batch_alter_table('doctor_specialties') as batch_op:
        batch_op.add_column(sa.Column('id', sa.String(), nullable=True))

    # generate id cho data cũ
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")
    op.execute("UPDATE doctor_specialties SET id = gen_random_uuid();")

    # set NOT NULL
    with op.batch_alter_table('doctor_specialties') as batch_op:
        batch_op.alter_column('id', nullable=False)

    # drop PK cũ và set PK mới
    op.execute("ALTER TABLE doctor_specialties DROP CONSTRAINT doctor_specialties_pkey;")
    op.execute("ALTER TABLE doctor_specialties ADD PRIMARY KEY (id);")

    # ================================
    # 2. APPOINTMENTS
    # ================================
    with op.batch_alter_table('appointments') as batch_op:
        batch_op.add_column(sa.Column('doctor_specialty_id', sa.String(), nullable=True))

    # (optional) nếu có data cũ thì map tạm
    # op.execute("UPDATE appointments SET doctor_specialty_id = ...")

    with op.batch_alter_table('appointments') as batch_op:
        batch_op.alter_column('doctor_specialty_id', nullable=False)
        batch_op.create_foreign_key(
            'fk_appointments_doctor_specialty',
            'doctor_specialties',
            ['doctor_specialty_id'],
            ['id']
        )

    # ================================
    # 3. DOCTOR_SCHEDULES
    # ================================
    with op.batch_alter_table('doctor_schedules') as batch_op:
        batch_op.add_column(sa.Column('doctor_specialty_id', sa.String(), nullable=True))

    with op.batch_alter_table('doctor_schedules') as batch_op:
        batch_op.drop_constraint(batch_op.f('doctor_schedules_doctor_id_fkey'), type_='foreignkey')
        batch_op.alter_column('doctor_specialty_id', nullable=False)
        batch_op.create_foreign_key(
            'fk_schedule_doctor_specialty',
            'doctor_specialties',
            ['doctor_specialty_id'],
            ['id']
        )
        batch_op.drop_column('doctor_id')

    # ================================
    # 4. TIME_SLOTS
    # ================================
    with op.batch_alter_table('time_slots') as batch_op:
        batch_op.add_column(sa.Column('doctor_specialty_id', sa.String(), nullable=True))

    with op.batch_alter_table('time_slots') as batch_op:
        batch_op.drop_constraint(batch_op.f('time_slots_doctor_id_fkey'), type_='foreignkey')
        batch_op.drop_index(batch_op.f('idx_doctor_date_available'))

        batch_op.alter_column('doctor_specialty_id', nullable=False)

        batch_op.create_foreign_key(
            'fk_timeslot_doctor_specialty',
            'doctor_specialties',
            ['doctor_specialty_id'],
            ['id']
        )

        batch_op.create_index(
            'idx_doctor_date_available',
            ['doctor_specialty_id', 'date', 'is_available'],
            unique=False
        )

        batch_op.drop_column('doctor_id')


def downgrade():
    # ================================
    # REVERT TIME_SLOTS
    # ================================
    with op.batch_alter_table('time_slots') as batch_op:
        batch_op.add_column(sa.Column('doctor_id', sa.String(), nullable=True))
        batch_op.drop_constraint('fk_timeslot_doctor_specialty', type_='foreignkey')
        batch_op.drop_index('idx_doctor_date_available')
        batch_op.create_index(
            'idx_doctor_date_available',
            ['doctor_id', 'date', 'is_available'],
            unique=False
        )
        batch_op.create_foreign_key(
            'time_slots_doctor_id_fkey',
            'doctors',
            ['doctor_id'],
            ['id']
        )
        batch_op.drop_column('doctor_specialty_id')

    # ================================
    # REVERT DOCTOR_SCHEDULES
    # ================================
    with op.batch_alter_table('doctor_schedules') as batch_op:
        batch_op.add_column(sa.Column('doctor_id', sa.String(), nullable=True))
        batch_op.drop_constraint('fk_schedule_doctor_specialty', type_='foreignkey')
        batch_op.create_foreign_key(
            'doctor_schedules_doctor_id_fkey',
            'doctors',
            ['doctor_id'],
            ['id']
        )
        batch_op.drop_column('doctor_specialty_id')

    # ================================
    # REVERT APPOINTMENTS
    # ================================
    with op.batch_alter_table('appointments') as batch_op:
        batch_op.drop_constraint('fk_appointments_doctor_specialty', type_='foreignkey')
        batch_op.drop_column('doctor_specialty_id')

    # ================================
    # REVERT doctor_specialties
    # ================================
    op.execute("ALTER TABLE doctor_specialties DROP CONSTRAINT doctor_specialties_pkey;")
    op.execute("ALTER TABLE doctor_specialties ADD PRIMARY KEY (doctor_id, specialty_id);")

    with op.batch_alter_table('doctor_specialties') as batch_op:
        batch_op.drop_column('id')