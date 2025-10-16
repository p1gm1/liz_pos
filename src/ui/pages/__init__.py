from .base_page import BasePage
from .product_management_page import ProductManagementPage

class PageRegistry:
    """Registry para gestionar páginas - OCP"""
    
    def __init__(self, app_state):
        self._pages = {}
        self._register_default_pages(app_state)
    
    def _register_default_pages(self, app_state) -> None:
        """Registra las páginas por defecto - OCP"""
        self.register(ProductManagementPage(app_state))
    
    def register(self, page: BasePage) -> None:
        """Registra una nueva página - OCP"""
        self._pages[page.get_display_name()] = page
    
    def get_page(self, page_name: str) -> BasePage:
        """Obtiene una página por nombre"""
        return self._pages.get(page_name)
    
    def get_page_names(self) -> list:
        """Obtiene todos los nombres de páginas"""
        return list(self._pages.keys())
    
    def get_default_page(self) -> BasePage:
        """Obtiene la página por defecto"""
        return list(self._pages.values())[0]