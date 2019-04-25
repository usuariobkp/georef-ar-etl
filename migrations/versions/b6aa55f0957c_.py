"""Create census localities

Revision ID: b6aa55f0957c
Revises: 45abb24d82b8
Create Date: 2019-04-24 14:36:40.487882

"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2


# revision identifiers, used by Alembic.
revision = 'b6aa55f0957c'
down_revision = '45abb24d82b8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('georef_localidades_censales',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('nombre', sa.String(), nullable=False),
    sa.Column('fuente', sa.String(), nullable=False),
    sa.Column('categoria', sa.String(), nullable=False),
    sa.Column('lon', sa.Float(), nullable=False),
    sa.Column('lat', sa.Float(), nullable=False),
    sa.Column('funcion', sa.String(), nullable=True),
    sa.Column('geometria', geoalchemy2.types.Geometry(geometry_type='POINT', srid=4326), nullable=False),
    sa.Column('provincia_id', sa.String(), nullable=False),
    sa.Column('departamento_id', sa.String(), nullable=True),
    sa.Column('municipio_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['departamento_id'], ['georef_departamentos.id'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['municipio_id'], ['georef_municipios.id'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['provincia_id'], ['georef_provincias.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('georef_localidades_censales')
    # ### end Alembic commands ###