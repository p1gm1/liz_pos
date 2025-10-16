# src/entities/base_entity.py
from abc import ABC
from datetime import datetime

class BaseEntity(ABC):
    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if not key.startswith('_')}

# src/entities/product.py
from .base_entity import BaseEntity

class Product(BaseEntity):
    def __init__(self, id: int = None, name: str = "", price: float = 0.0, 
                 stock: int = 0, tax_rate: float = 0.19, is_active: bool = True):
        self.id = id
        self.name = name
        self.price = price
        self.stock = stock
        self.tax_rate = tax_rate
        self.is_active = is_active

# src/entities/invoice.py
from datetime import datetime
from typing import List
from .base_entity import BaseEntity

class InvoiceItem(BaseEntity):
    def __init__(self, product_id: int, product_name: str, quantity: int, 
                 unit_price: float, tax_rate: float):
        self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity
        self.unit_price = unit_price
        self.tax_rate = tax_rate
        self.subtotal = quantity * unit_price
        self.tax_amount = self.subtotal * tax_rate
        self.total = self.subtotal + self.tax_amount

class Invoice(BaseEntity):
    def __init__(self, id: int = None, customer_document: str = "", 
                 customer_name: str = "Consumidor Final", invoice_number: str = ""):
        self.id = id
        self.customer_document = customer_document
        self.customer_name = customer_name
        self.invoice_number = invoice_number
        self.created_at = datetime.now()
        self.items: List[InvoiceItem] = []
        self.subtotal = 0.0
        self.tax_amount = 0.0
        self.total = 0.0
        self.status = "PENDING"  # PENDING, COMPLETED, CANCELLED
    
    def add_item(self, item: InvoiceItem):
        self.items.append(item)
        self._calculate_totals()
    
    def _calculate_totals(self):
        self.subtotal = sum(item.subtotal for item in self.items)
        self.tax_amount = sum(item.tax_amount for item in self.items)
        self.total = self.subtotal + self.tax_amount