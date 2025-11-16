# POS-POC - Punto de Venta (Prueba de Concepto)

## Funcionalidades Clave

### Gestión de Productos con XLSX

La página de "Gestión de Productos" ofrece potentes herramientas para actualizar el inventario masivamente usando archivos XLSX.

1.  **Eliminar Productos**: Permite eliminar productos de la base de datos en base a una lista de códigos de producto en un archivo XLSX.
2.  **Reconteo de Inventarios**: Una función de sincronización completa:
    -   **Añade y Actualiza**: Los productos en el archivo XLSX son añadidos a la base de datos si no existen, o actualizados si ya existen. El archivo debe contener columnas como `code`, `name`, `price`, etc.
    -   **Elimina**: Cualquier producto que exista en la base de datos pero no esté presente en el archivo XLSX será eliminado. Esto asegura que el inventario en la base de datos sea un reflejo exacto del contenido del archivo.

## Instalación y Ejecución

1.  **Clonar el repositorio:**
    ```bash
    git clone <URL-del-repositorio>
    cd liz-PoS
    ```

2.  **Instalar**
    * Si no tienes `uv` instalado, puedes instalarlo siguiendo las instrucciones en su [sitio web oficial](https://github.com/astral-sh/uv). 
    * Debes tener python

5.  **Ejecutar la aplicación:**
    Haz doble click en run_app.command

## Dependencias

Las dependencias del proyecto se gestionan con `uv` y están definidas en `pyproject.toml`. Las dependencias principales son:

-   `streamlit`: Para la creación de la interfaz de usuario web.
-   `sqlalchemy`: Para el ORM y la interacción con la base de datos.
-   `pandas`: Para la manipulación de datos, especialmente con archivos XLSX.
-   `openpyxl`: Requerido por `pandas` para trabajar con archivos Excel.

### Directorio `src`

Contiene todo el código fuente de la aplicación.

-   **`main.py`**: Punto de entrada principal de la aplicación Streamlit. Se encarga de inicializar la base de datos y renderizar la interfaz de usuario.
-   **`database/`**: Módulo para todo lo relacionado con la base de datos.
    -   `database.py`: Configuración de la conexión a la base de datos SQLite con SQLAlchemy.
    -   `models.py`: Define los modelos de datos (tablas) utilizando SQLAlchemy ORM.
    -   `migrations.py`: Script para manejar futuras migraciones de la base de datos.
-   **`entities/`**: Define las entidades de negocio principales de la aplicación (ej. `Product`).
-   **`repositories/`**: Capa de acceso a datos, responsable de la comunicación directa con la base de datos (operaciones CRUD).
-   **`services/`**: Capa de lógica de negocio. Coordina la interacción entre la UI y los repositorios.
-   **`ui/`**: Contiene todos los componentes de la interfaz de usuario construidos con Streamlit.
    -   `app_state.py`: Gestiona el estado de la aplicación.
    -   `sidebar.py`: Define la barra de navegación lateral.
    -   `components/`: Componentes de UI reutilizables (formularios, listas, etc.).
    -   `pages/`: Las diferentes páginas o vistas de la aplicación (ej. Gestión de Productos).
-   **`utils/`**: Utilidades y funciones auxiliares, como la configuración del logger.
