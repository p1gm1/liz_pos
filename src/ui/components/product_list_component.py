from typing import List, Callable, Optional

import streamlit as st
import pandas as pd

from src.entities.product import Product
from src.services.product_service import ProductService
from src.utils.logger import Logger


class ProductListComponent:
    """
    Componente especializado en mostrar listas de productos
    Responsabilidad Única: Renderizar y manejar interacciones de lista
    """
    
    def __init__(self, product_service: ProductService):
        self.product_service = product_service
        self.logger = Logger(__name__).get_logger()
    
    def render(self, 
               on_edit: Callable[[int], None],
               search_term: str = "") -> None:
        """Renderiza la lista de productos con opciones de búsqueda y acciones"""
        try:
            if st.session_state.get("product_to_delete"):
                self._confirm_delete()
                return

            products = self._load_products(search_term)
            
            if not products:
                self._render_empty_state()
                return
            
            self._render_search_header(len(products))
            self._render_products_table(products)
            self._render_actions_section(products, on_edit)
            
        except Exception as e:
            self.logger.error(f"Error rendering product list: {str(e)}")
            st.error("Error al cargar la lista de productos")
    
    def _load_products(self, search_term: str) -> List[Product]:
        """Carga productos según término de búsqueda"""
        if search_term and len(search_term.strip()) > 0:
            return self.product_service.search_products(search_term.strip())
        return self.product_service.get_all_products_any_status()
    
    def _render_empty_state(self) -> None:
        """Renderiza estado cuando no hay productos"""
        st.info("📭 No hay productos para mostrar.")
        st.markdown("""
        **Sugerencias:**
        - Verifica que los productos estén activos
        - Ajusta los términos de búsqueda
        - Agrega nuevos productos usando el formulario
        """)
    
    def _render_search_header(self, product_count: int) -> None:
        """Renderiza encabezado con información de búsqueda"""
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader("📋 Lista de Productos")
        with col2:
            st.metric("Productos", product_count)
    
    def _render_products_table(self, products: List[Product]) -> None:
        """Renderiza la tabla de productos optimizada"""
        # Preparar datos para DataFrame
        table_data = []
        for product in products:
            table_data.append({
                "ID": product.id,
                "Código": product.code or "N/A",
                "Nombre": product.name,
                "Precio": f"${product.price:,.2f}",
                "Categoría": product.category.value,
                "Estado": "✅ Activo" if product.is_active else "❌ Inactivo",
                "Creado": product.created_at.strftime("%Y-%m-%d %H:%M:%S") if product.created_at else "N/A",
                "Actualizado": product.updated_at.strftime("%Y-%m-%d %H:%M:%S") if product.updated_at else "N/A",
            })
        
        if table_data:
            df = pd.DataFrame(table_data)
            st.dataframe(
                df, 
                use_container_width=True, 
                hide_index=True,
            )
    
    def _render_actions_section(self, 
                              products: List[Product],
                              on_edit: Callable[[int], None]) -> None:
        """Renderiza sección de acciones para productos seleccionados"""
        st.markdown("---")
        st.subheader("🛠️ Acciones Rápidas")
        
        # Crear mapeo de productos para selección
        product_options = {
            p.id: f"{p.name} ({p.code})"
            for p in products
        }
        
        if not product_options:
            return
            
        selected_id = st.selectbox(
            "Seleccionar producto para acción:",
            options=list(product_options.keys()),
            format_func=lambda x: product_options[x],
            key="product_action_selector"
        )
        
        if selected_id:
            self._render_action_buttons(selected_id, on_edit)
    
    def _render_action_buttons(self, 
                             product_id: int,
                             on_edit: Callable[[int], None]) -> None:
        """Renderiza botones de acción para un producto específico"""
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✏️ Editar", key=f"edit_{product_id}", use_container_width=True):
                on_edit(product_id)
        
        with col2:
            if st.button("🗑️ Eliminar", key=f"delete_{product_id}", use_container_width=True):
                self._handle_delete_product(product_id)
    
    def _handle_delete_product(self, product_id: int) -> None:
        """Prepara el estado para la confirmación de eliminación"""
        st.session_state.product_to_delete = product_id
        st.rerun()

    def _confirm_delete(self) -> None:
        """Muestra el diálogo de confirmación y maneja la eliminación"""
        product_id = st.session_state.get("product_to_delete")
        if product_id is None:
            return

        try:
            product = self.product_service.get_product(product_id)
            if not product:
                st.error("El producto que intentas eliminar ya no existe.")
                st.session_state.product_to_delete = None
                st.rerun()
                return

            st.warning(f"### ¿Estás seguro de que deseas eliminar el producto?  \n**{product.name}** (Código: {product.code})  \nEsta acción es irreversible.")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Sí, eliminar", type="primary", use_container_width=True):
                    success = self.product_service.delete_product(product_id)
                    if success:
                        st.success(f"Producto '{product.name}' eliminado correctamente.")
                        st.session_state.product_to_delete = None
                        st.rerun()
                    else:
                        st.error("Ocurrió un error al eliminar el producto.")
            
            with col2:
                if st.button("❌ No, cancelar", use_container_width=True):
                    st.session_state.product_to_delete = None
                    st.rerun()

        except Exception as e:
            self.logger.error(f"Error during product deletion confirmation for product {product_id}: {e}")
            st.error("Se produjo un error inesperado durante la eliminación.")
            st.session_state.product_to_delete = None