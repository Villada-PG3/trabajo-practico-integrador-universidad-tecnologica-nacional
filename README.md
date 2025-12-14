🎓 Sistema Académico UTN

Este proyecto es un sistema académico desarrollado en Django para la Universidad Tecnológica Nacional, orientado a la gestión de carreras, alumnos, materias, cursos y profesores.
Permite administrar inscripciones, reinscripciones, asignación de docentes, carga de notas y visualización de información académica desde una plataforma web.

📂 Estructura relevante del Proyecto
---------------------------------------------------------------------
| Carpeta / Archivo     |                Descripción                | 
|-----------------------|-------------------------------------------|
| `TP_UTN/`             | Carpeta raíz del proyecto                 |
| `UTN/`                | App principal del sistema                 |
| `docs/`               | Documentación y diagramas (Mermaid, PNG)  |
| `UTN/static/`         | Archivos estáticos (CSS, imágenes, JS)    |
| `UTN/templates/ `     | Plantillas HTML                           |
| `templates/alumno/ `  | Vistas y templates del alumno             |
| `templates/carreras/ `| Listado y páginas individuales de carreras|
| `templates/materia/ ` | Gestión de materias                       |
|`templates/profesores/`| Panel y funciones de profesores           |
| `UTN/admin.py`        | Registro de modelos en el panel admin     |
| `UTN/apps.py`         | Configuración de la app                   |
| `UTN/forms.py`        | Formularios Django                        |
| `UTN/models.py`       | Modelos de la base de datos               |
| `UTN/views.py`        | Vistas del proyecto                       |
| `config/`             | Configuración general del proyecto Django |
| `venv/`               | Entorno virtual (no subir a Git)          |
---------------------------------------------------------------------


🛠 Requisitos

Python 3.12 o superior
Lenguaje principal del proyecto.

Django 5.2.5
Framework web utilizado para el desarrollo del sistema académico.

SQLite3
Motor de base de datos utilizado en entorno de desarrollo.

django-jazzmin
Tema visual para el panel de administración de Django.

social-auth-app-django
Autenticación mediante servicios externos (OAuth).

requests
Librería para manejo de peticiones HTTP (dependencia de autenticación externa).

Entorno virtual (venv)
Recomendado para aislar dependencias del proyecto.

⚡ Instalación y Ejecución
1️⃣ Clonar el repositorio
git clone <https://github.com/Villada-PG3/trabajo-practico-integrador-universidad-tecnologica-nacional.git>
cd TP_UTN

2️⃣ Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate

3️⃣ Instalar dependencias
pip install django

4️⃣ Ejecutar migraciones
python manage.py makemigrations
python manage.py migrate

5️⃣ Ejecutar servidor
python manage.py runserver

🔑 Panel de Administración

Nombre Super User: TP_UTN
Contraseña Super User: UTN

📜 Licencia

Proyecto de uso académico / escolar.
No destinado a producción.

🧑‍💻 Autores

Luciano Sibona
Facundo Peralta
Rodrigo Palacios
Tobias González Zar