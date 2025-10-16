from typing import List, Optional, Dict, Any

from src.entities.product import Product, ProductCategory
from src.repositories.product_repository import ProductRepository
from src.utils.logger import Logger


class ProductService:  
    """Implementación concreta del servicio de productos - Cumple SOLID"""
    
    def __init__(self, repository: ProductRepository):
        self.repository = repository
        self.logger = Logger(__name__).get_logger()
    
    def create_product(self, product_data: Dict[str, Any]) -> Product:
        """Crea producto con datos flexibles - Cumple OCP"""
        try:
            self._validate_required_fields(product_data)
            product: Product = self._build_product_from_data(product_data)

            is_valid, message = product.validate()
            if not is_valid:
                raise ValueError(f"Producto inválido: {message}")
            
            return self.repository.create(product)
            
        except Exception as e:
            self.logger.error(f"Error creating product: {str(e)}")
            raise
    
    def update_product(self, product_id: int, product_data: Dict[str, Any]) -> Optional[Product]:
        """Actualiza producto con datos flexibles - Cumple OCP"""
        try:
            product = self.repository.get_by_id(product_id)
            if not product:
                return None
            
            self._update_product_fields(product, product_data)
            
            is_valid, message = product.validate()
            if not is_valid:
                raise ValueError(f"Producto inválido después de actualizar: {message}")
            
            return self.repository.update(product)
            
        except Exception as e:
            self.logger.error(f"Error updating product {product_id}: {str(e)}")
            raise
    
    def _validate_required_fields(self, product_data: Dict[str, Any]) -> None:
        """Valida campos requeridos - Cumple SRP"""
        required_fields = [
            'code',
            'name',
            'description',
            'price',
            'cost',
            'category',
        ]
        missing_fields = [field for field in required_fields if field not in product_data]
        
        if missing_fields:
            raise ValueError(f"Campos requeridos faltantes: {', '.join(missing_fields)}")
    
    def _get_product_category(self, category_value: Any) -> ProductCategory:
        """Convierte un valor a ProductCategory de forma segura."""
        if isinstance(category_value, ProductCategory):
            return category_value
        
        if isinstance(category_value, str):
            try:
                return ProductCategory(category_value)
            except ValueError:
                self.logger.warning(f"Categoría '{category_value}' inválida. Usando categoría por defecto.")
        
        return ProductCategory.OTROS

    def _build_product_from_data(self, product_data: Dict[str, Any]) -> Product:
        """Construye entidad Product desde datos - Cumple SRP"""
        category = self._get_product_category(product_data.get('category'))

        # Mapear campos con valores por defecto
        product_kwargs = {
            'code': product_data['code'],
            'name': product_data['name'],
            'price': float(product_data['price']),
            'description': product_data.get('description', ''),
            'cost': float(product_data.get('cost', 0.0)),
            'category': category,
            'is_active': product_data.get('is_active', True)
        }
        
        return Product(**product_kwargs)
    
    def _update_product_fields(self, product: Product, product_data: Dict[str, Any]) -> None:
        """Actualiza campos del producto - Cumple SRP"""
        allowed_fields = [
            'code', 'name', 'description', 'price', 'cost',
            'category', 'is_active'
        ]
        
        for field, value in product_data.items():
            if field in allowed_fields and hasattr(product, field):
                if field in ['price', 'cost']:
                    value = float(value)
                elif field == 'is_active' and isinstance(value, str):
                    value = value.lower() == 'true'
                
                setattr(product, field, value)

    def get_product(self, product_id: int) -> Optional[Product]:
        return self.repository.get_by_id(product_id)
    
    def get_product_by_code(self, code: str) -> Optional[Product]:
        return self.repository.get_by_code(code)
    
    def get_all_products(self) -> List[Product]:
        return self.repository.get_all()
    
    def delete_product(self, product_id: int) -> bool:
        return self.repository.delete(product_id)

    def search_products(self, search_term: str) -> List[Product]:
        all_products = self.repository.get_all()
        search_term_lower = search_term.lower()
        
        return [
            product for product in all_products
            if (search_term_lower in product.name.lower() or 
                search_term_lower in (product.code or "").lower())
        ]
