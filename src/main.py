import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import streamlit as st

from src.ui.app_state import StreamlitAppState
from src.ui.pages import PageRegistry
from src.ui.sidebar import render_sidebar
from src.database.database import Database


def initialize_database():
    """Inicializa la base de datos con migraciones - SRP"""
    try:
        db = Database()
        db.create_tables()
        db.run_migrations()
        return True
    except Exception as e:
        st.error(f"Error al inicializar la base de datos: {e}")
        return False

def initialize_app() -> StreamlitAppState:
    """Inicializa la aplicación - SRP"""
    if 'app_state' not in st.session_state:
        st.session_state.app_state = StreamlitAppState()
    return st.session_state.app_state

def main():
    """Función principal de la aplicación - SRP"""
    st.set_page_config(
        page_title="Inventory Control",
        page_icon="📦", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("📦 Inventory Control")
    st.markdown("---")

    with st.spinner("Inicializando base de datos..."):
        if not initialize_database():
            st.error("No se pudo inicializar la base de datos. La aplicación no puede continuar.")
            return

    app_state = initialize_app()
    page_registry = PageRegistry(app_state)
    
    selected_page_name = render_sidebar(app_state, page_registry)

    selected_page = page_registry.get_page(selected_page_name)
    if selected_page:
        selected_page.render()
    else:
        st.error("Página no encontrada")

if __name__ == "__main__":
    main()