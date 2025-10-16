from typing import Optional

import streamlit as st
from abc import ABC, abstractmethod

from src.database.database import Database
from src.repositories.product_repository import ProductRepository
from src.services.product_service import ProductService
from src.utils.logger import Logger


class IAppState(ABC):
    """Interface para el estado de la aplicación - DIP"""
    
    @abstractmethod
    def get_product_service(self) -> ProductService:
        pass

    @abstractmethod
    def get_selected_product_id(self) -> Optional[int]:
        pass

    @abstractmethod
    def set_selected_product_id(self, product_id: Optional[int]) -> None:
        pass


class StreamlitAppState(IAppState):
    """Implementación concreta del estado para Streamlit - SRP"""
    
    def __init__(self):
        self.logger = Logger(__name__).get_logger()
        self._initialize_services()
    
    def _initialize_services(self):
        """Inicializa todos los servicios necesarios - SRP"""
        if 'product_service' not in st.session_state:
            db = Database()
            db.create_tables()
            session = db.get_session()
            
            # Repositories
            product_repo = ProductRepository(session)

            # Services
            product_service = ProductService(product_repo)
            
            # Session state
            st.session_state.product_service = product_service
            st.session_state.db_session = session
            
            # Estados de UI
            st.session_state.selected_product_id = None

            self.logger.info("Application services initialized")
    
    def get_product_service(self) -> ProductService:
        return st.session_state.product_service

    def get_selected_product_id(self) -> Optional[int]:
        return st.session_state.selected_product_id

    def set_selected_product_id(self, product_id: Optional[int]) -> None:
        st.session_state.selected_product_id = product_id