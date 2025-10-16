from typing import List, Optional

from sqlalchemy.orm import Session

from src.database.models import ProductModel
from src.entities.product import Product, ProductCategory
from .base_repository import BaseRepository


class ProductRepository(BaseRepository[Product]):
    def __init__(self, session: Session):
        super().__init__(session)
    
    def get_by_id(self, product_id: int) -> Optional[Product]:
        try:
            db_product = self.session.query(ProductModel).filter(ProductModel.id == product_id).first()
            if db_product:
                return self._to_entity(db_product)
            return None
        except Exception as e:
            self.logger.error(f"Error getting product by id {product_id}: {str(e)}")
            return None
    
    def get_by_code(self, code: str) -> Optional[Product]:
        """Obtiene producto por código"""
        try:
            db_product = self.session.query(ProductModel).filter(
                ProductModel.code == code,
                ProductModel.is_active == True
            ).first()
            if db_product:
                return self._to_entity(db_product)
            return None
        except Exception as e:
            self.logger.error(f"Error getting product by code {code}: {str(e)}")
            return None

    def get_by_code_any_status(self, code: str) -> Optional[Product]:
        """Obtiene producto por código sin importar su estado"""
        try:
            db_product = self.session.query(ProductModel).filter(
                ProductModel.code == code
            ).first()
            if db_product:
                return self._to_entity(db_product)
            return None
        except Exception as e:
            self.logger.error(f"Error getting product by code {code}: {str(e)}")
            return None
    
    def get_all(self) -> List[Product]:
        try:
            db_products = self.session.query(ProductModel).filter(ProductModel.is_active == True).all()
            return [self._to_entity(product) for product in db_products]
        except Exception as e:
            self.logger.error(f"Error getting all products: {str(e)}")
            return []

    def get_all_any_status(self) -> List[Product]:
        try:
            db_products = self.session.query(ProductModel).all()
            return [self._to_entity(product) for product in db_products]
        except Exception as e:
            self.logger.error(f"Error getting all products: {str(e)}")
            return []
    
    def create(self, entity: Product) -> Product:
        try:
            if entity.code:
                existing = self.get_by_code_any_status(entity.code)
                if existing:
                    raise ValueError(f"Ya existe un producto con el código: {entity.code}")
            
            db_product = self._to_model(entity)
            self.session.add(db_product)
            self.session.commit()
            self.session.refresh(db_product)
            
            entity.id = db_product.id
            self.logger.info(f"Product created: {entity.name} (ID: {entity.id})")
            return entity
            
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Error creating product: {str(e)}")
            raise
    
    def update(self, entity: Product) -> Product:
        try:
            db_product = self.session.query(ProductModel).filter(ProductModel.id == entity.id).first()
            if db_product:
                if entity.code and entity.code != db_product.code:
                    existing = self.get_by_code_any_status(entity.code)
                    if existing and existing.id != entity.id:
                        raise ValueError(f"Ya existe un producto con el código: {entity.code}")
                
                db_product.code = entity.code
                db_product.name = entity.name
                db_product.description = entity.description
                db_product.price = entity.price
                db_product.cost = entity.cost
                db_product.category = entity.category.value
                db_product.is_active = entity.is_active
                
                self.session.commit()
                self.logger.info(f"Product updated: {entity.name} (ID: {entity.id})")
            
            return entity
            
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Error updating product: {str(e)}")
            raise
    
    def delete(self, id: int) -> bool:
        try:
            db_product = self.session.query(ProductModel).filter(ProductModel.id == id).first()
            if db_product:
                db_product.is_active = False
                self.session.commit()
                self.logger.info(f"Product deleted: {id}")
                return True
            return False
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Error deleting product: {str(e)}")
            return False
    
    def update_stock(self, product_id: int, new_stock: int) -> bool:
        """Actualiza el stock de un producto"""
        try:
            db_product = self.session.query(ProductModel).filter(ProductModel.id == product_id).first()
            if db_product:
                db_product.stock = new_stock
                self.session.commit()
                self.logger.info(f"Stock updated for product {product_id}: {new_stock}")
                return True
            return False
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Error updating stock for product {product_id}: {str(e)}")
            return False
    
    def _to_entity(self, db_product: ProductModel) -> Product:
        """Convierte modelo de base de datos a entidad"""
        return Product(
            id=db_product.id,
            code=db_product.code,
            name=db_product.name,
            description=db_product.description,
            price=db_product.price,
            cost=db_product.cost,
            category=ProductCategory(db_product.category),
            is_active=db_product.is_active,
            created_at=db_product.created_at
        )
    
    def _to_model(self, entity: Product) -> ProductModel:
        """Convierte entidad a modelo de base de datos"""
        return ProductModel(
            code=entity.code,
            name=entity.name,
            description=entity.description,
            price=entity.price,
            cost=entity.cost,
            category=entity.category.value,
            is_active=entity.is_active
        )