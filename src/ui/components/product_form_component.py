from typing import Optional, Dict, Callable

import streamlit as st

from src.entities.product import Product, ProductCategory
from src.utils.logger import Logger


class ProductFormComponent:
    """
    Componente especializado en formularios de productos
    Responsabilidad Única: Renderizar y validar formularios de productos
    """
    
    def __init__(self):
        self.logger = Logger(__name__).get_logger()
    
    def render(self, 
               product: Optional[Product],
               on_save: Callable[[Dict], None],
               on_cancel: Callable[[], None]) -> None:
        """Renderiza el formulario de producto"""
        is_editing = product is not None
        
        st.subheader("✏️ Editar Producto" if is_editing else "➕ Añadir Nuevo Producto")
        
        with st.form(key="product_form", clear_on_submit=not is_editing):
            form_data = self._render_form_fields(product)
            
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                if st.form_submit_button(
                    "💾 Guardar Cambios" if is_editing else "✅ Crear Producto",
                    type="primary",
                    use_container_width=True
                ):
                    self._handle_form_submission(form_data, on_save)
            
            with col2:
                if st.form_submit_button("🔄 Limpiar", use_container_width=True):
                    st.rerun()
            
            with col3:
                if st.form_submit_button("❌ Cancelar", type="secondary", use_container_width=True):
                    on_cancel()
    
    def _render_form_fields(self, product: Optional[Product]) -> Dict:
        """Renderiza los campos del formulario y retorna los datos"""
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input(
                "📛 Nombre del Producto *",
                value=product.name if product else "",
                placeholder="Ej: Café Premium 500g",
                help="Nombre descriptivo del producto"
            )
            
            code = st.text_input(
                "🏷️ Código del Producto",
                value=product.code if product else "",
                placeholder="Ej: CAFE-PREM-500",
                help="Código único identificador (opcional)"
            )
        
        with col2:
            category = self._render_category_select(product)
            is_active = self._render_status_toggle(product)
        
        st.markdown("### 💰 Información de Precios")
        col1, col2 = st.columns(2)
        
        with col1:
            price = st.number_input(
                "Precio de Venta *",
                min_value=0.0,
                value=float(product.price) if product else 0.0,
                step=0.5,
                format="%.2f",
                help="Precio al que se vende el producto"
            )
        
        with col2:
            cost = st.number_input(
                "Costo del Producto",
                min_value=0.0,
                value=float(product.cost) if product else 0.0,
                step=0.5,
                format="%.2f",
                help="Costo de adquisición del producto"
            )

        description = st.text_area(
            "📝 Descripción del Producto",
            value=product.description if product else "",
            placeholder="Descripción detallada del producto...",
            height=100
        )
        
        return {
            "name": name,
            "code": code,
            "price": price,
            "cost": cost,
            "category": category,
            "is_active": is_active,
            "description": description
        }
    
    def _render_category_select(self, product: Optional[Product]) -> ProductCategory:
        """Renderiza el selector de categoría"""
        current_value = product.category.value if product else ProductCategory.OTROS.value
        category_options = [category.value for category in ProductCategory]
        
        try:
            current_index = category_options.index(current_value)
        except ValueError:
            current_index = 0
        
        selected_category = st.selectbox(
            "📂 Categoría *",
            options=category_options,
            index=current_index,
            help="Categoría del producto para organización"
        )
        
        return ProductCategory(selected_category)
    
    def _render_status_toggle(self, product: Optional[Product]) -> bool:
        """Renderiza el toggle de estado activo/inactivo"""
        is_active = product.is_active if product else True
        
        return st.toggle(
            "Estado del Producto",
            value=is_active,
            help="Producto activo/inactivo en el sistema"
        )
    
    def _handle_form_submission(self, form_data: Dict, on_save: Callable[[Dict], None]) -> None:
        """Maneja el envío del formulario con validación"""
        try:

            if not form_data["name"] or not form_data["name"].strip():
                st.error("❌ El nombre del producto es obligatorio")
                return
            
            if form_data["price"] <= 0:
                st.error("❌ El precio debe ser mayor a cero")
                return
            
            if form_data["stock"] < 0:
                st.error("❌ El stock no puede ser negativo")
                return
            
            # Si pasa todas las validaciones, llamar al callback
            on_save(form_data)
            
        except Exception as e:
            self.logger.error(f"Error in form submission: {str(e)}")
            st.error(f"❌ Error al procesar el formulario: {str(e)}")