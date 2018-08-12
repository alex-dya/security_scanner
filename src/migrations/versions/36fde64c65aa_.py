"""empty message

Revision ID: 36fde64c65aa
Revises: bd6687dcade8
Create Date: 2018-08-12 20:41:42.371988

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '36fde64c65aa'
down_revision = 'bd6687dcade8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('host_result',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('config', sa.String(), nullable=True),
    sa.Column('hostname', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['task_id'], ['task_result.id'], name='host_result_fk', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('celery_tasksetmeta')
    op.drop_table('celery_taskmeta')
    op.add_column('control_result', sa.Column('host_result_id', sa.Integer(), nullable=False))
    op.drop_constraint('control_result_fk', 'control_result', type_='foreignkey')
    op.create_foreign_key('control_result_fk', 'control_result', 'host_result', ['host_result_id'], ['id'], ondelete='CASCADE')
    op.drop_column('control_result', 'task_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('control_result', sa.Column('task_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint('control_result_fk', 'control_result', type_='foreignkey')
    op.create_foreign_key('control_result_fk', 'control_result', 'task_result', ['task_id'], ['id'], ondelete='CASCADE')
    op.drop_column('control_result', 'host_result_id')
    op.create_table('celery_taskmeta',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('task_id', sa.VARCHAR(length=155), autoincrement=False, nullable=True),
    sa.Column('status', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('result', postgresql.BYTEA(), autoincrement=False, nullable=True),
    sa.Column('date_done', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('traceback', sa.TEXT(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='celery_taskmeta_pkey'),
    sa.UniqueConstraint('task_id', name='celery_taskmeta_task_id_key')
    )
    op.create_table('celery_tasksetmeta',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('taskset_id', sa.VARCHAR(length=155), autoincrement=False, nullable=True),
    sa.Column('result', postgresql.BYTEA(), autoincrement=False, nullable=True),
    sa.Column('date_done', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='celery_tasksetmeta_pkey'),
    sa.UniqueConstraint('taskset_id', name='celery_tasksetmeta_taskset_id_key')
    )
    op.drop_table('host_result')
    # ### end Alembic commands ###
