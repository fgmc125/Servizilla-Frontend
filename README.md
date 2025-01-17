# Plataforma de Servicios Comunitarios - Frontend

Este repositorio contiene el frontend para la plataforma digital que conecta a vecinos del barrio **Las Flores** que ofrecen y buscan servicios o conocimientos. El frontend se desarrolla utilizando **Flet**, una biblioteca de Python para construir interfaces de usuario multiplataforma, orientada a ofrecer una experiencia intuitiva y accesible.

## **Objetivo**
El objetivo principal del frontend es proporcionar una interfaz moderna y fácil de usar para que los vecinos puedan publicar, buscar, solicitar y coordinar servicios o conocimientos de manera eficiente.

## **Características Principales**
- **Gestión de Usuarios**:
  - Registro e inicio de sesión para oferentes, buscadores o ambos.
  - Manejo de tokens de acceso (JWT) proporcionados por la API del backend.
- **Publicación de Servicios**:
  - Interfaz para crear, editar y eliminar servicios.
  - Listado de servicios disponibles con detalles relevantes.
- **Búsqueda y Solicitudes**:
  - Búsqueda de servicios por palabras clave y filtros avanzados.
  - Funcionalidad para enviar solicitudes a los servicios seleccionados.
- **Mensajería**:
  - Interfaz de chat para coordinar detalles del servicio entre buscadores y oferentes.
- **Calificaciones y Comentarios**:
  - Sección para calificar servicios y dejar comentarios sobre la experiencia.

## **Tecnologías Utilizadas**
- **Lenguaje**: Python 3.10+
- **Framework**: Flet
- **API Backend**: Django REST Framework (con integración JWT)

## **Instalación y Configuración**
### **Requisitos Previos**
- Python 3.10 o superior
- pip (administrador de paquetes de Python)
- Virtualenv (recomendado para crear un entorno virtual)

### **Instrucciones**
1. Clona el repositorio:
   ```bash
   git clone https://github.com/fgmc125/Servizilla-Frontend.git
   cd project
   ```

2. Crea un entorno virtual e instálalo:
    ```bash
    python3 -m venv env
    source env/bin/activate  # En Windows: .\env\Scripts\activate
    ```

3. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

4. Ejecuta la aplicación:
    ```bash
    flet main.py
    ```

## Estructura del Proyecto
  ```bash
  frontend/
  ├── src/                          # Carpeta principal del código fuente.
  │   ├── assets/                   # Recursos estáticos como imágenes e íconos.
  │   │   └── logo.svg              # Logotipo principal de la aplicación.
  │   │   └── splash_screen.png     # Imagen para la pantalla de inicio.
  │   ├── components/               # Componentes reutilizables (botones, tarjetas, etc.).
  │   │   └── navegation_hub.py     # Componente para gestionar la navegación lateral.
  │   ├── layouts/                  # Layouts o plantillas generales para las páginas.
  │   │   └── common_layout.py      # Estructura común para páginas generales.
  │   │   └── dashboard_layout.py   # Estructura específica para el dashboard.
  │   │   └── faq_layout.py         # Estructura para la página de preguntas frecuentes.
  │   │   └── home_layout.py        # Layout para la página principal.
  │   │   └── layout.py             # Base para manejar y renderizar layouts dinámicamente.
  │   ├── managers/                 # Objetos para manejar lógica principal y el flujo del sistema.
  │   │   └── app_manager.py        # Orquestador principal que controla el estado y las interacciones.
  │   ├── helpers/                  # Objetos para manejar lógica común.
  │   │   └── LayoutHandler.py      # Manejador para actualizar y coordinar cambios en los layouts.
  │   │   └── ResizeHandler.py      # Manejador de eventos de cambio de tamaño de ventana.
  │   │   └── RouteHandler.py       # Manejador de rutas dinámicas.
  │   │   └── SessionHandler.py     # Manejador del estado de sesión y autenticación.
  │   │   └── StateHandler.py       # Manejador del estado global de la aplicación.
  │   ├── contents/                 # Contenido cargado dinámicamente dentro de los layouts.
  │   │   ├── login.py              # Contenido para la autenticación (inicio de sesión).
  │   │   ├── signup.py             # Contenido para el registro de usuarios.
  │   │   ├── dashboard.py          # Contenido para la gestión de servicios y solicitudes.
  │   │   ├── home.py               # Contenido de la página principal.
  │   │   └── miscellaneous.py      # Contenido adicional para páginas no categorizadas.
  │   ├── routes/                   # Definición de rutas para navegación.
  │   │   └── routes.py             # Archivo que define las rutas de la aplicación.
  │   ├── services/                 # Lógica para las llamadas a la API.
  │   │   └── api_client.py         # Cliente para realizar peticiones al backend.
  │   ├── utils/                    # Funciones utilitarias (e.g., manejo de tokens, configuración).
  │   │   └── logger.py             # Herramienta para registrar eventos y errores.
  │   ├── project.log               # Archivo de registro con eventos y errores del proyecto.
  ├── main.py                       # Archivo principal para ejecutar la aplicación.
  ├── project.log                   # Archivo de registro general del proyecto.
  ├── pyproject.toml                # Archivo de configuración para herramientas de Python.
  ├── README.md                     # Documentación del proyecto.
  ├── requirements.txt              # Dependencias del proyecto.
  ├── settings.py                   # Configuración general del proyecto (e.g., API_BASE_URL).
  ```

## Conexión con el Backend
El frontend consume la API REST proporcionada por el backend para realizar operaciones como:

* Autenticación: Inicio de sesión y manejo de tokens JWT.
* Servicios: Listar, crear, editar, eliminar y buscar servicios.
* Solicitudes: Enviar solicitudes y listar las realizadas.
* Mensajes: Coordinación entre oferentes y buscadores.

## Interacción con la API
### Ejemplo de Configuración
La base URL de la API debe configurarse en el proyecto (por ejemplo, en un archivo config.py):

```python
API_BASE_URL = "http://127.0.0.1:8000/api/"
```

## Flujo de Trabajo del Frontend
1. Inicio de Sesión:
  * El usuario se autentica a través de la API (POST /auth/token/) y recibe un token JWT.
2. Gestión de Servicios:
  * El frontend realiza llamadas a los endpoints del backend para listar, crear, editar o eliminar servicios.
3. Solicitudes y Mensajería:
  * Las solicitudes y mensajes se gestionan mediante peticiones a la API en tiempo real o asincrónicamente.

## Licencia
Este proyecto está protegido por una Licencia de Uso Propietaria. Todos los derechos sobre el software son propiedad exclusiva de Reploid IT.
El uso, copia o distribución del software sin autorización está estrictamente prohibido. Consulta el archivo LICENSE para más detalles.

## Contacto
Para consultas o soporte, contacta a:

Coordinadora del Proyecto: Martínez Dante, Martínez Cruz, Flavio G.
Desarrolladores: Reploid Dev
