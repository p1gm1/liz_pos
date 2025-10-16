from sqlalchemy import create_engine, MetaData, Table, Column
from sqlalchemy.engine import reflection

def upgrade(db_uri="sqlite:///pos_system.db"):
    """
    Upgrades the database to the latest version.
    """
    engine = create_engine(db_uri)
    meta = MetaData()

    with engine.connect() as connection:
        inspector = reflection.Inspector.from_engine(connection)
        if 'products' in inspector.get_table_names():
            meta.reflect(bind=engine)
            products_table = Table('products', meta, autoload_with=engine)

def downgrade(db_uri="sqlite:///pos_system.db"):
    """
    Downgrades the database to the previous version.
    """
    engine = create_engine(db_uri)
    meta = MetaData()

    with engine.connect() as connection:
        inspector = reflection.Inspector.from_engine(connection)
        if 'products' in inspector.get_table_names():
            meta.reflect(bind=engine)
            products_table = Table('products', meta, autoload_with=engine)
