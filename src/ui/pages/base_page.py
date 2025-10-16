from abc import ABC, abstractmethod
from src.ui.app_state import IAppState


class BasePage(ABC):
    """Clase base abstracta para todas las páginas - OCP, LSP"""
    
    def __init__(self, app_state: IAppState):
        self.app_state = app_state
    
    @abstractmethod
    def render(self) -> None:
        """Renderiza el contenido de la página"""
        pass
    
    @property
    @abstractmethod
    def title(self) -> str:
        """Título de la página para el menú"""
        pass
    
    @property
    @abstractmethod
    def icon(self) -> str:
        """Ícono de la página para el menú"""
        pass
    
    def get_display_name(self) -> str:
        """Nombre completo para mostrar en el menú"""
        return f"{self.icon} {self.title}"