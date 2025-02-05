"""v3.10: Add container tables (tokencontainer, tokencontainerinfo, tokencontainerowner, tokencontainerrealm,
tokencontainerstates, tokencontainertoken) and add columns container_serial and container_type to the privacy_idea
audit table.

Revision ID: 69e7817b9863
Revises: 2100d1fad908
Create Date: 2024-07-05 10:05:13.987514

"""
from sqlalchemy.exc import OperationalError, ProgrammingError

# revision identifiers, used by Alembic.
revision = '69e7817b9863'
down_revision = '2100d1fad908'

from alembic import op
import sqlalchemy as sa


def upgrade():
    try:
        # ### commands auto generated by Alembic - please adjust! ###
        op.create_table('tokencontainer',
                        sa.Column('id', sa.Integer(), sa.Identity(always=False), nullable=False),
                        sa.Column('type', sa.Unicode(length=100), nullable=False),
                        sa.Column('description', sa.Unicode(length=1024), nullable=True),
                        sa.Column('serial', sa.Unicode(length=40), nullable=False),
                        sa.Column('last_seen', sa.DateTime(), nullable=True),
                        sa.Column('last_updated', sa.DateTime(), nullable=True),
                        sa.PrimaryKeyConstraint('id'),
                        mysql_row_format='DYNAMIC'
                        )
        op.create_index(op.f('ix_tokencontainer_serial'), 'tokencontainer', ['serial'], unique=True)
    except (OperationalError, ProgrammingError) as exx:
        if "already exists" in str(exx.orig).lower():
            print("Table 'tokencontainer' already exists.")
        else:
            print("Could not add table 'tokencontainer' to database.")
            print(exx)

    try:
        op.create_table('tokencontainerinfo',
                        sa.Column('id', sa.Integer(), sa.Identity(always=False), nullable=False),
                        sa.Column('key', sa.Unicode(length=255), nullable=False),
                        sa.Column('value', sa.UnicodeText(), nullable=True),
                        sa.Column('type', sa.Unicode(length=100), nullable=True),
                        sa.Column('description', sa.Unicode(length=2000), nullable=True),
                        sa.Column('container_id', sa.Integer(), nullable=True),
                        sa.ForeignKeyConstraint(['container_id'], ['tokencontainer.id'], ),
                        sa.PrimaryKeyConstraint('id'),
                        sa.UniqueConstraint('container_id', 'key', name='container_id_constraint'),
                        mysql_row_format='DYNAMIC'
                        )
        op.create_index(op.f('ix_tokencontainerinfo_container_id'), 'tokencontainerinfo', ['container_id'],
                        unique=False)
    except (OperationalError, ProgrammingError) as exx:
        if "already exists" in str(exx.orig).lower():
            print("Table 'tokencontainerinfo' already exists.")
        else:
            print("Could not add table 'tokencontainerinfo' to database.")
            print(exx)

    try:
        op.create_table('tokencontainerowner',
                        sa.Column('id', sa.Integer(), sa.Identity(always=False), nullable=False),
                        sa.Column('container_id', sa.Integer(), nullable=True),
                        sa.Column('resolver', sa.Unicode(length=120), nullable=True),
                        sa.Column('user_id', sa.Unicode(length=320), nullable=True),
                        sa.Column('realm_id', sa.Integer(), nullable=True),
                        sa.ForeignKeyConstraint(['container_id'], ['tokencontainer.id'], ),
                        sa.ForeignKeyConstraint(['realm_id'], ['realm.id'], ),
                        sa.PrimaryKeyConstraint('id'),
                        mysql_row_format='DYNAMIC'
                        )
        op.create_index(op.f('ix_tokencontainerowner_resolver'), 'tokencontainerowner', ['resolver'], unique=False)
        op.create_index(op.f('ix_tokencontainerowner_user_id'), 'tokencontainerowner', ['user_id'], unique=False)
    except (OperationalError, ProgrammingError) as exx:
        if "already exists" in str(exx.orig).lower():
            print("Table 'tokencontainerowner' already exists.")
        else:
            print("Could not add table 'tokencontainerowner' to database.")
            print(exx)

    try:
        op.create_table('tokencontainerrealm',
                        sa.Column('container_id', sa.Integer(), nullable=False),
                        sa.Column('realm_id', sa.Integer(), nullable=False),
                        sa.ForeignKeyConstraint(['container_id'], ['tokencontainer.id'], ),
                        sa.ForeignKeyConstraint(['realm_id'], ['realm.id'], ),
                        sa.PrimaryKeyConstraint('container_id', 'realm_id'),
                        mysql_row_format='DYNAMIC'
                        )
    except (OperationalError, ProgrammingError) as exx:
        if "already exists" in str(exx.orig).lower():
            print("Table 'tokencontainerrealm' already exists.")
        else:
            print("Could not add table 'tokencontainerrealm' to database.")
            print(exx)

    try:
        op.create_table('tokencontainerstates',
                        sa.Column('id', sa.Integer(), sa.Identity(always=False), nullable=False),
                        sa.Column('container_id', sa.Integer(), nullable=True),
                        sa.Column('state', sa.Unicode(length=100), nullable=False),
                        sa.ForeignKeyConstraint(['container_id'], ['tokencontainer.id'], ),
                        sa.PrimaryKeyConstraint('id'),
                        mysql_row_format='DYNAMIC'
                        )
    except (OperationalError, ProgrammingError) as exx:
        if "already exists" in str(exx.orig).lower():
            print("Table 'tokencontainerstates' already exists.")
        else:
            print("Could not add table 'tokencontainerstates' to database.")
            print(exx)

    try:
        op.create_table('tokencontainertoken',
                        sa.Column('token_id', sa.Integer(), nullable=False),
                        sa.Column('container_id', sa.Integer(), nullable=False),
                        sa.ForeignKeyConstraint(['container_id'], ['tokencontainer.id'], ),
                        sa.ForeignKeyConstraint(['token_id'], ['token.id'], ),
                        sa.PrimaryKeyConstraint('token_id', 'container_id'),
                        mysql_row_format='DYNAMIC'
                        )
    except (OperationalError, ProgrammingError) as exx:
        if "already exists" in str(exx.orig).lower():
            print("Table 'tokencontainertoken' already exists.")
        else:
            print("Could not add table 'tokencontainertoken' to database.")
            print(exx)

    try:
        op.add_column('pidea_audit', sa.Column('container_serial', sa.Unicode(20), nullable=True))
    except (OperationalError, ProgrammingError) as exx:
        if "already exists" in str(exx.orig).lower() or "duplicate column name" in str(exx.orig).lower():
            print("Columns 'container_serial' already exist.")
        else:
            print("Could not add columns 'container_serial' to table 'pidea_audit'.")
            print(exx)

    try:
        op.add_column('pidea_audit', sa.Column('container_type', sa.Unicode(20), nullable=True))
    except (OperationalError, ProgrammingError) as exx:
        if "already exists" in str(exx.orig).lower() or "duplicate column name" in str(exx.orig).lower():
            print("Columns 'container_type' already exist.")
        else:
            print("Could not add columns 'container_type' to table 'pidea_audit'.")
            print(exx)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    try:
        op.drop_column('pidea_audit', 'container_type')
    except (OperationalError, ProgrammingError) as exx:
        msg = str(exx.orig).lower()
        if "no such column" in msg or "does not exist" in msg:
            print("Column 'container_type' already removed.")
        else:
            print("Could not remove column 'container_type' from table 'pidea_audit'.")
            print(exx)

    try:
        op.drop_column('pidea_audit', 'container_serial')
    except (OperationalError, ProgrammingError) as exx:
        msg = str(exx.orig).lower()
        if "no such column" in msg or "does not exist" in msg:
            print("Column 'container_serial' already removed.")
        else:
            print("Could not remove column 'container_serial' from table 'pidea_audit'.")
            print(exx)

    try:
        op.drop_table('tokencontainertoken')
    except (OperationalError, ProgrammingError) as exx:
        msg = str(exx.orig).lower()
        if "no such table" in msg or "unknown table" in msg or "does not exist" in msg:
            print("Table 'tokencontainertoken' already removed.")
        else:
            print("Could not remove table 'tokencontainertoken'.")
            print(exx)

    try:
        op.drop_table('tokencontainerstates')
    except (OperationalError, ProgrammingError) as exx:
        msg = str(exx.orig).lower()
        if "no such table" in msg or "unknown table" in msg or "does not exist" in msg:
            print("Table 'tokencontainerstates' already removed.")
        else:
            print("Could not remove table 'tokencontainerstates'.")
            print(exx)

    try:
        op.drop_table('tokencontainerrealm')
    except (OperationalError, ProgrammingError) as exx:
        msg = str(exx.orig).lower()
        if "no such table" in msg or "unknown table" in msg or "does not exist" in msg:
            print("Table 'tokencontainerrealm' already removed.")
        else:
            print("Could not remove table 'tokencontainerrealm'.")
            print(exx)

    try:
        op.drop_index(op.f('ix_tokencontainerowner_user_id'), table_name='tokencontainerowner')
    except (OperationalError, ProgrammingError) as exx:
        msg = str(exx.orig).lower()
        if "no such index" in msg or "does not exist" in msg:
            print("Index 'ix_tokencontainerowner_user_id' already removed.")
        else:
            print("Could not remove index 'ix_tokencontainerowner_user_id' from table 'tokencontainerowner'.")
            print(exx)

    try:
        op.drop_index(op.f('ix_tokencontainerowner_resolver'), table_name='tokencontainerowner')
    except (OperationalError, ProgrammingError) as exx:
        msg = str(exx.orig).lower()
        if "no such index" in msg or "does not exist" in msg:
            print("Index 'ix_tokencontainerowner_resolver' already removed.")
        else:
            print("Could not remove index 'ix_tokencontainerowner_resolver' from table 'tokencontainerowner'.")
            print(exx)

    try:
        op.drop_table('tokencontainerowner')
    except (OperationalError, ProgrammingError) as exx:
        msg = str(exx.orig).lower()
        if "no such table" in msg or "unknown table" in msg or "does not exist" in msg:
            print("Table 'tokencontainerowner' already removed.")
        else:
            print("Could not remove table 'tokencontainerowner'.")
            print(exx)

    try:
        op.drop_index(op.f('ix_tokencontainerinfo_container_id'), table_name='tokencontainerinfo')
    except (OperationalError, ProgrammingError) as exx:
        msg = str(exx.orig).lower()
        if "no such index" in msg or "does not exist" in msg:
            print("Index 'ix_tokencontainerinfo_container_id' already removed.")
        else:
            print("Could not remove index 'ix_tokencontainerinfo_container_id' from table 'tokencontainerinfo'.")
            print(exx)

    try:
        op.drop_table('tokencontainerinfo')
    except (OperationalError, ProgrammingError) as exx:
        msg = str(exx.orig).lower()
        if "no such table" in msg or "unknown table" in msg or "does not exist" in msg:
            print("Table 'tokencontainerinfo' already removed.")
        else:
            print("Could not remove table 'tokencontainerinfo'.")
            print(exx)

    try:
        op.drop_index(op.f('ix_tokencontainer_serial'), table_name='tokencontainer')
    except (OperationalError, ProgrammingError) as exx:
        msg = str(exx.orig).lower()
        if "no such index" in msg or "does not exist" in msg:
            print("Index 'ix_tokencontainer_serial' already removed.")
        else:
            print("Could not remove index 'ix_tokencontainer_serial' from table 'tokencontainer'.")
            print(exx)

    try:
        op.drop_table('tokencontainer')
    except (OperationalError, ProgrammingError) as exx:
        msg = str(exx.orig).lower()
        if "no such table" in msg or "unknown table" in msg or "does not exist" in msg:
            print("Table 'tokencontainer' already removed.")
        else:
            print("Could not remove table 'tokencontainer'.")
    # ### end Alembic commands ###
