# src/ui/pages/product_management_page.py
from typing import Optional

import streamlit as st
import pandas as pd

from .base_page import BasePage
from src.ui.app_state import IAppState
from src.entities.product import Product
from src.services.product_service import ProductService
from src.ui.components.product_list_component import ProductListComponent
from src.ui.components.product_form_component import ProductFormComponent
from src.utils.logger import Logger


class ProductManagementPage(BasePage):
    """
    Página de gestión de productos - Coordina componentes especializados
    Responsabilidad Única: Coordinación entre componentes y estado
    """
    
    def __init__(self, app_state: IAppState):
        super().__init__(app_state)
        self._title = "Gestión de Productos"
        self._icon = "📦"
        self.logger = Logger(__name__).get_logger()
        
        # Inyección de dependencias
        self.product_service: ProductService = self.app_state.get_product_service()
        
        # Composición de componentes especializados
        self.list_component = ProductListComponent(self.product_service)
        self.form_component = ProductFormComponent()
        
        # Estado de la página
        self._current_view = "list"
        self._selected_product_id: Optional[int] = None

    @property
    def title(self) -> str:
        return self._title

    @property
    def icon(self) -> str:
        return self._icon

    def render(self) -> None:
        """Método principal de renderizado - Coordina componentes"""
        try:
            self._setup_initial_state()
            self._render_page_header()
            self._render_navigation()
            self._render_current_view()
            
        except Exception as e:
            self.logger.error(f"Error in product management page: {str(e)}")
            st.error("❌ Error al cargar la página de gestión de productos")

    def _setup_initial_state(self) -> None:
        """Configura el estado inicial de la página"""
        if "product_mgmt_view" not in st.session_state:
            st.session_state.product_mgmt_view = "list"
        
        app_product_id = self.app_state.get_selected_product_id()
        if app_product_id is not None:
            self._selected_product_id = app_product_id
            st.session_state.product_mgmt_view = "form"

    def _render_page_header(self) -> None:
        """Renderiza el encabezado de la página"""
        st.header(self.get_display_name())
        st.markdown("---")

    def _render_navigation(self) -> None:
        """Renderiza la navegación entre vistas"""
        st.sidebar.markdown("### 🧭 Navegación")
        
        view_options = {
            "list": "📋 Ver Productos",
            "form": "✏️ Gestionar Producto", 
        }
        
        selected_view = st.sidebar.radio(
            "Seleccionar Vista:",
            options=list(view_options.keys()),
            format_func=lambda x: view_options[x],
            index=list(view_options.keys()).index(st.session_state.product_mgmt_view)
        )
        
        if selected_view != st.session_state.product_mgmt_view:
            st.session_state.product_mgmt_view = selected_view
            if selected_view != "form":
                self._clear_product_selection()
            st.rerun()

    def _render_current_view(self) -> None:
        """Renderiza la vista actual basada en el estado"""
        current_view = st.session_state.product_mgmt_view
        
        if current_view == "list":
            self._render_list_view()
        elif current_view == "form":
            self._render_form_view()

    def _render_list_view(self) -> None:
        """Renderiza la vista de lista de productos"""
        st.markdown("""
            <style>
            .green-buttons .stButton > button {
                background-color: #4CAF50; /* Green */
                color: white;
            }
            </style>
        """, unsafe_allow_html=True)

        search_term = st.text_input(
            "🔍 Buscar productos...",
            placeholder="Buscar por nombre, código o categoría...",
            key="product_search_main"
        )
        
        self.list_component.render(
            on_edit=self._handle_edit_product,
            search_term=search_term
        )

        st.markdown("---")
        st.subheader("Actualización de Inventario por XLSX")

        xlsx_action = st.selectbox(
            "Seleccione la acción a realizar con el XLSX:",
            ("Eliminar productos", "Reconteo de Inventarios")
        )

        uploaded_file = st.file_uploader(
            "Selecciona un archivo XLSX",
            type=["xlsx"],
            key=f"xlsx_uploader_{xlsx_action}" # Unique key
        )

        if uploaded_file:
            st.markdown("""<style>
                        div.stButton > button:first-child {
                            background-color: #00FF00; /* Green background */
                            color: white; /* White text */
                        }
                        </style>'""", unsafe_allow_html=True)
            if xlsx_action == "Salida de productos":
                st.button(
                    "🔄️ Registra salida de productos desde XLSX",
                    on_click=self._handle_xlsx_upload,
                    args=(uploaded_file,),
                    key="xlsx_delete_button"
                )
            elif xlsx_action == "Reconteo de Inventarios":
                st.button(
                    "🔄 Realizar Reconteo de Inventarios",
                    on_click=self._handle_inventory_recount_xlsx,
                    args=(uploaded_file,),
                    key="xlsx_recount_button"
                )

    def _render_form_view(self) -> None:
        """Renderiza la vista de formulario de producto"""
        product = self._get_current_product()
        
        if self._selected_product_id and not product:
            st.error("❌ El producto seleccionado no existe")
            self._clear_product_selection()
            st.rerun()
            return
        
        self.form_component.render(
            product=product,
            on_save=self._handle_save_product,
            on_cancel=self._handle_cancel_form
        )

    def _get_current_product(self) -> Optional[Product]:
        """Obtiene el producto actualmente seleccionado"""
        if self._selected_product_id:
            return self.product_service.get_product(self._selected_product_id)
        return None

    def _get_product_display_name(self, product_id: int) -> str:
        """Obtiene nombre para display de un producto"""
        product = self.product_service.get_product(product_id)
        if product:
            return f"{product.name} ({product.code})"
        return f"Producto #{product_id}"

    def _handle_edit_product(self, product_id: int) -> None:
        """Maneja la edición de un producto"""
        self._selected_product_id = product_id
        self.app_state.set_selected_product_id(product_id)
        st.session_state.product_mgmt_view = "form"
        st.rerun()

    def _handle_save_product(self, form_data: dict) -> None:
        """Maneja el guardado de productos - CORREGIDO"""
        try:
            if self._selected_product_id:
                # Edición
                self.product_service.update_product(self._selected_product_id, form_data)
                st.success("✅ Producto actualizado correctamente")
            else:
                # Creación - envía todo el diccionario
                self.product_service.create_product(form_data)
                st.success("✅ Producto creado correctamente")
            
            self._clear_product_selection()
            st.session_state.product_mgmt_view = "list"
            st.rerun()
        
        except ValueError as e:
            st.error(f"❌ Error de validación: {e}")
        except Exception as e:
            self.logger.error(f"Error saving product: {str(e)}")
            st.error(f"❌ Error al guardar el producto: {str(e)}")

    def _handle_xlsx_upload(self, uploaded_file) -> None:
        """Maneja la subida de un XLSX para eliminar productos."""
        if not uploaded_file:
            st.warning("Por favor, sube un archivo XLSX.")
            return

        try:
            df = pd.read_excel(uploaded_file, engine='openpyxl')

            if "code" not in df.columns:
                st.error("El archivo XLSX debe contener la columna 'code'.")
                return

            deleted_count = 0
            not_found_codes = []
            processed_codes = set()

            for code in df["code"]:
                code_str = str(code)
                if code_str in processed_codes:
                    continue
                
                product = self.product_service.get_product_by_code(code_str)
                
                if product:
                    self.product_service.delete_product(product.id)
                    deleted_count += 1
                else:
                    not_found_codes.append(code_str)
                
                processed_codes.add(code_str)

            if deleted_count > 0:
                st.success(f"{deleted_count} productos eliminados correctamente.")
            
            if not_found_codes:
                st.warning(f"No se encontraron los siguientes códigos: {', '.join(not_found_codes)}")

            st.rerun()

        except Exception as e:
            self.logger.error(f"Error al procesar el archivo XLSX: {e}")
            st.error(f"Ocurrió un error al procesar el archivo: {e}")

    def _handle_cancel_form(self) -> None:
        """Maneja la cancelación del formulario"""
        self._clear_product_selection()
        st.session_state.product_mgmt_view = "list"
        st.rerun()

    def _handle_inventory_recount_xlsx(self, uploaded_file) -> None:
        """
        Maneja la subida de un XLSX para realizar un reconteo de inventario.
        Añade productos nuevos, actualiza existentes y elimina los que no están en el archivo.
        """
        if not uploaded_file:
            st.warning("Por favor, sube un archivo XLSX.")
            return

        try:
            df = pd.read_excel(uploaded_file, engine='openpyxl')

            required_columns = ["code", "name"]
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                st.error(f"El archivo XLSX debe contener las siguientes columnas: {', '.join(missing_columns)}")
                return

            added_count = 0
            updated_count = 0
            deleted_count = 0
            processed_codes = set()

            # Añadir y actualizar productos
            for index, row in df.iterrows():
                code = str(row["code"])
                if code in processed_codes:
                    continue
                
                processed_codes.add(code)
                existing_product = self.product_service.get_product_by_code_any_status(code)

                if existing_product:
                    # Actualizar producto existente
                    product_data = {}
                    for col in df.columns:
                        if col != "code" and pd.notna(row[col]):
                            product_data[col] = row[col]
                    
                    if "is_active" not in product_data:
                        product_data["is_active"] = True

                    if product_data:
                        self.product_service.update_product(existing_product.id, product_data)
                        updated_count += 1
                else:
                    # Añadir nuevo producto
                    name = row.get("name", "")
                    description = row.get("description")
                    price = row.get("price")
                    cost = row.get("cost")
                    category = row.get("category")

                    product_data = {
                        "code": code,
                        "name": str(name) if pd.notna(name) else "null",
                        "description": str(description) if pd.notna(description) else "null",
                        "price": float(price) if pd.notna(price) else 0.0,
                        "cost": float(cost) if pd.notna(cost) else 0.0,
                        "category": str(category) if pd.notna(category) else "Otros",
                        "is_active": True
                    }
                    self.product_service.create_product(product_data)
                    added_count += 1

            # Eliminar productos que no están en el XLSX
            db_products = self.product_service.get_all_products_any_status()
            db_codes = {p.code for p in db_products}
            
            codes_to_delete = db_codes - processed_codes

            for code in codes_to_delete:
                product_to_delete = self.product_service.get_product_by_code_any_status(code)
                if product_to_delete:
                    self.product_service.delete_product(product_to_delete.id)
                    deleted_count += 1

            if added_count > 0:
                st.success(f"{added_count} nuevos productos añadidos correctamente.")
            if updated_count > 0:
                st.success(f"{updated_count} productos actualizados correctamente.")
            if deleted_count > 0:
                st.success(f"{deleted_count} productos eliminados correctamente.")
            
            if added_count == 0 and updated_count == 0 and deleted_count == 0:
                st.info("No se realizaron cambios en el inventario.")

            st.rerun()

        except Exception as e:
            self.logger.error(f"Error al procesar el archivo XLSX para reconteo: {e}")
            st.error(f"Ocurrió un error al procesar el archivo: {e}")

    def _clear_product_selection(self) -> None:
        """Limpia la selección de producto"""
        self._selected_product_id = None
        self.app_state.set_selected_product_id(None)
