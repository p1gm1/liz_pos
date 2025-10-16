from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from src.utils.logger import Logger

logger = Logger(__name__).get_logger()

Base = declarative_base()


class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        self.engine = create_engine('sqlite:///pos_system.db', echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        logger.info("Database singleton initialized successfully")
    
    def get_session(self):
        return self.SessionLocal()
    
    def create_tables(self):
        from src.database import models
        Base.metadata.create_all(bind=self.engine)
        logger.info("Database tables created successfully")
    
    def run_migrations(self):
        """Ejecuta migraciones automáticamente - SOLUCIÓN AL PROBLEMA"""
        session = self.get_session()
        try:
            result = session.execute(text("PRAGMA table_info(products)"))
            columns = [row[1] for row in result]
            
            if 'supplier' not in columns:
                logger.info("🔄 Ejecutando migración: agregando columna 'supplier'...")
                session.execute(text("ALTER TABLE products ADD COLUMN supplier VARCHAR(200)"))
                session.commit()
                logger.info("✅ Migración completada: columna 'supplier' agregada")
            else:
                logger.info("✅ Columna 'supplier' ya existe en la base de datos")
                
        except Exception as e:
            logger.error(f"❌ Error en migración: {e}")
            session.rollback()
            raise
        finally:
            session.close()