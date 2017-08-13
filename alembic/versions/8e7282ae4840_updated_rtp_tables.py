"""updated rtp tables

Revision ID: 8e7282ae4840
Revises: e66c069eb92b
Create Date: 2017-08-13 18:06:40.892734+00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8e7282ae4840'
down_revision = 'e66c069eb92b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('host_status')
    op.add_column('rtp_process_record', sa.Column('hera_cal_git_hash', sa.String(length=64), nullable=False))
    op.add_column('rtp_process_record', sa.Column('hera_cal_git_version', sa.String(length=32), nullable=False))
    op.add_column('rtp_process_record', sa.Column('hera_qm_git_hash', sa.String(length=64), nullable=False))
    op.add_column('rtp_process_record', sa.Column('hera_qm_git_version', sa.String(length=32), nullable=False))
    op.add_column('rtp_process_record', sa.Column('pyuvdata_git_hash', sa.String(length=64), nullable=False))
    op.add_column('rtp_process_record', sa.Column('pyuvdata_git_version', sa.String(length=32), nullable=False))
    op.add_column('rtp_process_record', sa.Column('rtp_git_hash', sa.String(length=64), nullable=False))
    op.add_column('rtp_process_record', sa.Column('rtp_git_version', sa.String(length=32), nullable=False))
    op.drop_column('rtp_process_record', 'git_hash')
    op.drop_column('rtp_process_record', 'git_version')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rtp_process_record', sa.Column('git_version', sa.VARCHAR(length=32), autoincrement=False, nullable=False))
    op.add_column('rtp_process_record', sa.Column('git_hash', sa.VARCHAR(length=64), autoincrement=False, nullable=False))
    op.drop_column('rtp_process_record', 'rtp_git_version')
    op.drop_column('rtp_process_record', 'rtp_git_hash')
    op.drop_column('rtp_process_record', 'pyuvdata_git_version')
    op.drop_column('rtp_process_record', 'pyuvdata_git_hash')
    op.drop_column('rtp_process_record', 'hera_qm_git_version')
    op.drop_column('rtp_process_record', 'hera_qm_git_hash')
    op.drop_column('rtp_process_record', 'hera_cal_git_version')
    op.drop_column('rtp_process_record', 'hera_cal_git_hash')
    op.create_table('host_status',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('hostname', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('load_average', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('uptime', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name=u'host_status_pkey')
    )
    # ### end Alembic commands ###
