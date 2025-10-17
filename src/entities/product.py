from typing import Optional
from enum import Enum

from .base_entity import BaseEntity


class ProductCategory(Enum):
    FILTROS = "Filtros"
    HERRAMIENTAS = "Herramientas"
    OTROS = "Otros"


class Product(BaseEntity):
    def __init__(self, id: int = None, code: str = "", name: str = "", description: str = "",
                 price: float = 0.0, cost: float = 0.0,
                 category: ProductCategory = ProductCategory.OTROS,
                 is_active: bool = True, created_at: Optional[str] = None, updated_at: Optional[str] = None):
        
        self.id = id
        self.code = code
        self.name = name
        self.description = description
        self.price = price
        self.cost = cost
        self.category = category
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at

    def validate(self) -> tuple[bool, str]:
        errors = []
        if not self.name or len(self.name.strip()) == 0:
            errors.append("El nombre del producto es requerido")
        if self.price < 0:
            errors.append("El precio no puede ser negativo")

        if errors:
            return False, ", ".join(errors)
        
        return True, "Producto válido"