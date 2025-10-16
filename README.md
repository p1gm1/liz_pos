# POS-POC - Punto de Venta (Prueba de Concepto)

## Descripción General

Este proyecto es una Prueba de Concepto (POC) de un sistema de Punto de Venta (POS) simple, diseñado para ser compatible con las regulaciones de la DIAN en Colombia. La aplicación está construida con Python y Streamlit, y utiliza una base de datos SQLite para almacenar la información de productos, clientes y facturas.

## Estructura del Proyecto

A continuación se describe la función de cada archivo dentro del proyecto:

- **`.gitignore`**: Especifica los archivos y directorios que Git debe ignorar. Esto es útil para evitar que archivos temporales, dependencias y otros archivos no esenciales se incluyan en el control de versiones.
- **`app.py`**: Es el punto de entrada principal de la aplicación Streamlit. Se encarga de la navegación entre las diferentes páginas (módulos) de la aplicación, como el Dashboard, Punto de Venta, Gestión de Productos, etc.
- **`container.py`**: Implementa un contenedor de inyección de dependencias. Se encarga de instanciar y gestionar las dependencias de la aplicación, como los servicios y repositorios, asegurando que cada componente reciba las instancias que necesita para funcionar.
- **`database.py`**: Contiene la configuración y gestión de la conexión a la base de datos SQLite. Define el motor de SQLAlchemy, la sesión de la base de datos y funciones para inicializar la base de datos.
- **`database_setup.py`**: Script utilizado para inicializar o recrear la base de datos. Utiliza las definiciones de `database.py` y `models.py` para crear las tablas necesarias.
- **`models.py`**: Define los modelos de datos de la aplicación utilizando SQLAlchemy ORM. Aquí se definen las tablas `productos`, `clientes`, `facturas` y `factura_items` con sus respectivas columnas y relaciones.
- **`pytest.ini`**: Archivo de configuración para Pytest. Permite definir opciones y configuraciones para la ejecución de las pruebas unitarias.
- **`python-3.12.8-amd64.exe`**: Instalador de Python. No es parte del código fuente del proyecto.
- **`README.md`**: Este archivo. Contiene la documentación del proyecto.
- **`requirements.txt`**: Lista todas las dependencias de Python necesarias para ejecutar el proyecto. Se utiliza para instalar las librerías con `pip install -r requirements.txt`.

### Directorio `pages`

Este directorio contiene los diferentes módulos o páginas de la aplicación Streamlit.

- **`__init__.py`**: Archivo vacío que indica a Python que el directorio `pages` es un paquete.
- **`advanced_reports.py`**: Módulo para generar reportes avanzados. (Actualmente vacío o con funcionalidad limitada).
- **`customer_management.py`**: Módulo para la gestión de clientes. Permite crear, editar y eliminar clientes.
- **`dashboard.py`**: Página principal de la aplicación. Muestra un resumen general de la información del sistema, como ventas recientes, productos más vendidos, etc.
- **`invoice_history.py`**: Módulo para ver el historial de facturas generadas.
- **`point_of_sale.py`**: Módulo principal del Punto de Venta. Permite seleccionar productos, asociar un cliente y generar una nueva factura.
- **`product_management.py`**: Módulo para la gestión de productos. Permite crear, editar y eliminar productos del inventario.

### Directorio `repository`

Este directorio contiene la capa de acceso a datos. Se encarga de la comunicación directa con la base de datos.

- **`__init__.py`**: Archivo vacío que indica a Python que el directorio `repository` es un paquete.
- **`base_repository.py`**: Define la interfaz base para los repositorios. (Actualmente vacío o con funcionalidad limitada).
- **`sqlite_repository.py`**: Implementación del repositorio para una base de datos SQLite. Contiene la lógica para realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) en la base de datos.

### Directorio `services`

Este directorio contiene la lógica de negocio de la aplicación.

- **`__init__.py`**: Archivo vacío que indica a Python que el directorio `services` es un paquete.
- **`customer_service.py`**: Contiene la lógica de negocio para la gestión de clientes. Actúa como intermediario entre la interfaz de usuario y el repositorio de clientes.
- **`invoice_service.py`**: Contiene la lógica de negocio para la gestión de facturas. Se encarga de crear nuevas facturas, calcular totales y generar el texto de la factura.
- **`product_service.py`**: Contiene la lógica de negocio para la gestión de productos.

### Directorio `tests`

Este directorio contiene las pruebas unitarias del proyecto.

- **`conftest.py`**: Archivo de configuración para Pytest. Permite definir fixtures y otras configuraciones para las pruebas.
- **`test_customer_service.py`**: Pruebas unitarias para `CustomerService`.
- **`test_example_unittest.py`**: Archivo de ejemplo de pruebas unitarias.
- **`test_product_service.py`**: Pruebas unitarias para `ProductService`.

### Directorio `utils`

Este directorio contiene utilidades y funciones auxiliares utilizadas en todo el proyecto.

- **`__init__.py`**: Archivo vacío que indica a Python que el directorio `utils` es un paquete.
- **`logger.py`**: Configuración del sistema de logging para registrar eventos y errores de la aplicación.
- **`validators.py`**: Funciones para validar datos, como formatos de correo electrónico, números de documento, etc. (Actualmente vacío o con funcionalidad limitada).

## Instalación y Ejecución

1.  **Clonar el repositorio:**
    ```bash
    git clone <URL-del-repositorio>
    cd POS-POC
    ```

2.  **Crear un entorno virtual:**
    ```bash
    python -m venv .venv
    ```

3.  **Activar el entorno virtual:**
    -   En Windows:
        ```bash
        .venv\Scripts\activate
        ```
    -   En macOS y Linux:
        ```bash
        source .venv/bin/activate
        ```

4.  **Instalar las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Inicializar la base de datos:**
    ```bash
    python database_setup.py
    ```

6.  **Ejecutar la aplicación:**
    ```bash
    streamlit run app.py
    ```

## Dependencias

Las dependencias del proyecto se encuentran en el archivo `requirements.txt` y se pueden instalar con `pip`. Las dependencias principales son:

- `streamlit`: Para la creación de la interfaz de usuario web.
- `SQLAlchemy`: Para el ORM y la interacción con la base de datos.
- `pandas`: Para la manipulación y visualización de datos.
- `pytest`: Para la ejecución de pruebas unitarias.