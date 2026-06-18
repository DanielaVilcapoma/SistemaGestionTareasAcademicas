# SistemaGestionTareasAcademicas
📌 Sistema de Gestión de Tareas Académicas

Este proyecto es un sistema desarrollado en Python para la gestión de tareas académicas, implementando control de versiones con Git y GitHub, flujo de trabajo GitFlow e integración continua (CI/CD) mediante GitHub Actions.

🚀 Funcionalidades
Registro de tareas académicas
Listado de tareas registradas
Búsqueda de tareas
Edición y actualización de tareas
Cambio de estado (pendiente / completado)
Eliminación de tareas
🛠️ Tecnologías utilizadas
Python
Git
GitHub
GitHub Actions (CI/CD)
🌿 Flujo de trabajo (GitFlow)

El proyecto utiliza GitFlow para la organización del desarrollo:

main: versión estable del sistema
develop: rama de desarrollo
feature/*: desarrollo de nuevas funcionalidades
⚙️ Integración continua (CI/CD)

Se implementó GitHub Actions para automatizar la ejecución del sistema en cada actualización del repositorio.

El pipeline ejecuta automáticamente el archivo app.py para validar su funcionamiento.

▶️ Ejecución del proyecto

Para ejecutar el sistema de forma local:

python app.py
📂 Estructura del proyecto
SistemaGestionTareasAcademicas/
│
├── app.py
├── README.md
└── .github/
    └── workflows/
        └── python-ci.yml
👤 Autor

Daniela Vilcapoma

📌 Nota

Este proyecto fue desarrollado como parte de una evaluación académica aplicando buenas prácticas de desarrollo de software, control de versiones y automatización de procesos.
