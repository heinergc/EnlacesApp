# 🔗 Aplicación Web de Gestión de Enlaces

Una aplicación web moderna y autocontenida para gestionar y organizar tus enlaces web favoritos por categorías. Construida con Flask, SQLite y Bootstrap 5.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.2-purple.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey.svg)

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Capturas de Pantalla](#-capturas-de-pantalla)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [API Endpoints](#-api-endpoints)
- [Tecnologías](#-tecnologías)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)

## ✨ Características

### Funcionalidades Principales

- **Dashboard Interactivo**: Visualiza todas tus categorías en tarjetas elegantes
- **CRUD Completo de Categorías**: Crea, lee, actualiza y elimina categorías
- **CRUD Completo de Enlaces**: Gestiona todos tus enlaces web favoritos
- **Organización por Categorías**: Agrupa tus enlaces de forma lógica
- **Vista Detallada**: Explora todos los enlaces de cada categoría
- **Interfaz Responsiva**: Diseño adaptable a cualquier dispositivo
- **Base de Datos Local**: Almacenamiento seguro con SQLite
- **Búsqueda Rápida**: Encuentra tus enlaces fácilmente
- **Notificaciones Toast**: Feedback visual de todas las operaciones

### Características Técnicas

- API RESTful completa
- Validación de datos en frontend y backend
- Manejo robusto de errores
- Eliminación en cascada de datos relacionados
- Diseño modular y escalable
- Código limpio y documentado

## 📸 Capturas de Pantalla

### Dashboard Principal
Visualiza todas tus categorías con la cantidad de enlaces que contienen.

### Vista de Categoría
Explora todos los enlaces organizados por categoría.

### Modales de Edición
Interfaz intuitiva para crear y editar categorías y enlaces.

## 🔧 Requisitos

### Software Necesario

- **Python 3.8 o superior**
- **pip** (gestor de paquetes de Python)
- Navegador web moderno (Chrome, Firefox, Edge, Safari)

### Requisitos del Sistema

- **Windows 10/11** (recomendado) o Linux/macOS
- **100 MB** de espacio en disco
- **2 GB RAM** (mínimo)

## 📥 Instalación

### Windows

1. **Clonar o descargar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd EnlacesApp
   ```

2. **Ejecutar el script de inicio**
   ```cmd
   run.bat
   ```

   El script automáticamente:
   - Verificará la instalación de Python
   - Creará un entorno virtual
   - Instalará las dependencias
   - Iniciará el servidor

3. **Abrir en el navegador**
   ```
   http://localhost:5000
   ```

### Linux/macOS

1. **Clonar o descargar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd EnlacesApp
   ```

2. **Ejecutar el script de inicio**
   ```bash
   ./run.sh
   ```

   El script automáticamente:
   - Verificará la instalación de Python
   - Creará un entorno virtual
   - Instalará las dependencias
   - Iniciará el servidor

3. **Abrir en el navegador**
   ```
   http://localhost:5000
   ```

### Instalación Manual

Si prefieres instalar manualmente:

```bash
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/macOS:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la aplicación
python app.py
```

## 🚀 Uso

### Gestión de Categorías

#### Crear una Categoría
1. Haz clic en el botón **"Nueva Categoría"** en el dashboard
2. Ingresa el nombre de la categoría
3. Haz clic en **"Guardar"**

#### Editar una Categoría
1. Haz clic en el menú de tres puntos (⋮) en la tarjeta de la categoría
2. Selecciona **"Editar"**
3. Modifica el nombre
4. Haz clic en **"Guardar"**

#### Eliminar una Categoría
1. Haz clic en el menú de tres puntos (⋮) en la tarjeta de la categoría
2. Selecciona **"Eliminar"**
3. Confirma la eliminación
   > ⚠️ **Advertencia**: Esto eliminará la categoría y todos sus enlaces

### Gestión de Enlaces

#### Crear un Enlace
1. Entra a una categoría haciendo clic en **"Ver Enlaces"**
2. Haz clic en **"Nuevo Enlace"**
3. Completa el formulario:
   - **Título**: Nombre descriptivo del enlace
   - **URL**: Dirección web completa
   - **Categoría**: Selecciona la categoría (predeterminada: actual)
4. Haz clic en **"Guardar"**

#### Editar un Enlace
1. Haz clic en el menú de tres puntos (⋮) en la tarjeta del enlace
2. Selecciona **"Editar"**
3. Modifica los campos necesarios
4. Haz clic en **"Guardar"**

#### Eliminar un Enlace
1. Haz clic en el menú de tres puntos (⋮) en la tarjeta del enlace
2. Selecciona **"Eliminar"**
3. Confirma la eliminación

#### Abrir un Enlace
1. Haz clic en el botón **"Abrir Enlace"** en la tarjeta
2. El enlace se abrirá en una nueva pestaña

## 📁 Estructura del Proyecto

```
EnlacesApp/
│
├── app.py                 # Aplicación Flask principal
├── models.py              # Modelos de base de datos (SQLAlchemy)
├── database.py            # Configuración e inicialización de BD
├── requirements.txt       # Dependencias de Python
├── .gitignore            # Archivos ignorados por Git
├── README.md             # Documentación del proyecto
│
├── run.bat               # Script de inicio para Windows
├── run.sh                # Script de inicio para Linux/macOS
│
├── static/               # Archivos estáticos
│   ├── css/
│   │   └── style.css    # Estilos personalizados
│   └── js/
│       └── main.js      # JavaScript personalizado
│
└── templates/            # Plantillas HTML
    ├── base.html        # Plantilla base
    ├── index.html       # Dashboard principal
    └── categoria.html   # Vista de categoría detallada
```

## 🔌 API Endpoints

### Categorías

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/categorias` | Obtener todas las categorías |
| GET | `/api/categorias/<id>` | Obtener una categoría específica |
| POST | `/api/categorias` | Crear nueva categoría |
| PUT | `/api/categorias/<id>` | Actualizar categoría |
| DELETE | `/api/categorias/<id>` | Eliminar categoría |

### Enlaces

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/enlaces` | Obtener todos los enlaces |
| GET | `/api/enlaces?categoria_id=<id>` | Obtener enlaces de una categoría |
| GET | `/api/enlaces/<id>` | Obtener un enlace específico |
| POST | `/api/enlaces` | Crear nuevo enlace |
| PUT | `/api/enlaces/<id>` | Actualizar enlace |
| DELETE | `/api/enlaces/<id>` | Eliminar enlace |

### Ejemplos de Uso de la API

#### Crear una Categoría
```javascript
fetch('/api/categorias', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        nombre: 'Desarrollo'
    })
})
```

#### Crear un Enlace
```javascript
fetch('/api/enlaces', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        titulo: 'GitHub',
        url: 'https://github.com',
        categoria_id: 1
    })
})
```

## 🛠️ Tecnologías

### Backend
- **Flask 3.0.0**: Framework web minimalista
- **Flask-SQLAlchemy 3.1.1**: ORM para manejo de base de datos
- **SQLite**: Base de datos local embebida
- **Python 3.8+**: Lenguaje de programación

### Frontend
- **Bootstrap 5.3.2**: Framework CSS responsivo
- **Bootstrap Icons**: Iconografía moderna
- **JavaScript ES6+**: Funcionalidades dinámicas
- **HTML5 & CSS3**: Estructura y estilos

### Herramientas de Desarrollo
- **Git**: Control de versiones
- **pip**: Gestor de paquetes de Python
- **venv**: Entornos virtuales de Python

## 🐛 Solución de Problemas

### La aplicación no inicia

**Error**: `Python no está instalado`
- **Solución**: Instala Python 3.8 o superior desde [python.org](https://www.python.org)

**Error**: `No se pudieron instalar las dependencias`
- **Solución**: Verifica tu conexión a internet y ejecuta manualmente:
  ```bash
  pip install -r requirements.txt
  ```

### No se puede acceder a la aplicación

**Problema**: El navegador no carga `http://localhost:5000`
- **Solución 1**: Verifica que el servidor esté corriendo (debe mostrar el mensaje de inicio)
- **Solución 2**: Intenta con otra dirección: `http://127.0.0.1:5000`
- **Solución 3**: Verifica que el puerto 5000 no esté siendo usado por otra aplicación

### Errores de base de datos

**Problema**: Error al crear/actualizar datos
- **Solución**: Elimina el archivo `enlaces.db` y reinicia la aplicación
  ```bash
  # En Windows
  del enlaces.db

  # En Linux/macOS
  rm enlaces.db
  ```

## 🤝 Contribuir

Las contribuciones son bienvenidas. Para contribuir:

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/NuevaCaracteristica`)
3. Commit tus cambios (`git commit -m 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## 👤 Autor

Creado con ❤️ por [Tu Nombre]

## 🙏 Agradecimientos

- Bootstrap por el framework CSS
- Flask por el framework web
- La comunidad de Python por las excelentes herramientas

---

**¿Preguntas o sugerencias?** Abre un issue en el repositorio.

**¿Te gusta el proyecto?** Dale una ⭐ en GitHub.
