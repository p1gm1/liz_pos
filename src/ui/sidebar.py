import streamlit as st

from src.ui.app_state import StreamlitAppState
from src.ui.pages import PageRegistry


def render_sidebar(app_state: StreamlitAppState, page_registry: PageRegistry) -> str:
    """Renderiza la sidebar y retorna la página seleccionada - SRP"""
    with st.sidebar:
        st.header("Panel de Control")
        
        st.markdown("---")

        st.markdown("### Navegación")
        selected_page = st.selectbox(
            "Menú Principal", 
            page_registry.get_page_names()
        )
    
    return selected_page
