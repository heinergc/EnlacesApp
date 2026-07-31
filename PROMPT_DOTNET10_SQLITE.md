# Prompt: Gestión de Enlaces con .NET 10 LTS y SQLite

Quiero que construyas una aplicación web completa llamada **“Gestión de Enlaces”**, utilizando exclusivamente:

- .NET 10 LTS
- ASP.NET Core MVC
- Entity Framework Core 10
- SQLite
- Razor Views
- Tailwind CSS
- JavaScript moderno sin frameworks
- xUnit para pruebas

## Objetivo

Crear una aplicación local, moderna y responsive para guardar, organizar, buscar y administrar enlaces web agrupados por categorías.

La interfaz debe estar completamente en español.

## Requisitos funcionales

### 1. Gestión de categorías

Permitir:

- Listar categorías ordenadas alfabéticamente.
- Crear categorías.
- Consultar una categoría.
- Editar categorías.
- Eliminar categorías.
- Eliminar automáticamente todos los enlaces asociados cuando se elimina una categoría.
- Impedir categorías con nombres duplicados, ignorando mayúsculas y minúsculas.
- Mostrar en cada categoría:
  - Nombre.
  - Icono.
  - Color.
  - Cantidad de enlaces.
  - Cantidad de favoritos.
  - Fecha de creación.

### 2. Gestión de enlaces

Permitir:

- Listar todos los enlaces.
- Filtrar enlaces por categoría.
- Crear enlaces.
- Consultar un enlace.
- Editar enlaces.
- Mover un enlace a otra categoría.
- Eliminar enlaces.
- Marcar o desmarcar enlaces como favoritos.
- Abrir enlaces en una pestaña nueva.
- Registrar la cantidad de clics.
- Registrar la fecha y hora del último acceso.
- Agregar descripción y etiquetas.
- Buscar enlaces por título, URL, descripción y etiquetas.

Si una URL no contiene protocolo, agregar automáticamente `https://`.

Solo aceptar URLs HTTP o HTTPS válidas.

### 3. Dashboard

Crear un dashboard que muestre:

- Total de categorías.
- Total de enlaces.
- Total de favoritos.
- Total de clics.
- Los 10 enlaces más visitados.
- Los 10 enlaces creados recientemente.
- Las 5 categorías con más enlaces.
- Una sección de enlaces favoritos.
- Un buscador global.
- Acceso rápido para abrir cada enlace.

### 4. Importación y exportación

Permitir:

- Exportar todas las categorías y enlaces a JSON.
- Descargar el archivo exportado desde el navegador.
- Importar información desde un archivo JSON.
- Validar rigurosamente la estructura del archivo.
- Crear las categorías inexistentes durante la importación.
- Evitar enlaces duplicados usando la URL normalizada.
- Ejecutar toda la importación dentro de una transacción.
- Mostrar la cantidad de categorías y enlaces importados.
- Establecer un tamaño máximo razonable para los archivos importados.

## Modelo de datos

Crear la entidad `Categoria` con:

- `Id`: entero, clave primaria.
- `Nombre`: string requerido, máximo 100 caracteres, único.
- `Icono`: string, máximo 50 caracteres, valor predeterminado `📁`.
- `Color`: string de 7 caracteres, valor predeterminado `#667eea`.
- `FechaCreacionUtc`: `DateTimeOffset`.
- Colección de enlaces.

Crear la entidad `Enlace` con:

- `Id`: entero, clave primaria.
- `Titulo`: string requerido, máximo 200 caracteres.
- `Url`: string requerido, máximo 2048 caracteres.
- `Descripcion`: string, máximo 2000 caracteres.
- `CategoriaId`: clave foránea requerida.
- `Favorito`: booleano, valor predeterminado `false`.
- `Clicks`: entero no negativo.
- `Tags`: string, máximo 500 caracteres, o una entidad separada si resulta más limpio.
- `FechaCreacionUtc`: `DateTimeOffset`.
- `FechaUltimoAccesoUtc`: `DateTimeOffset` nullable.
- Navegación hacia `Categoria`.

Configura índices para:

- Nombre de categoría único con comparación adecuada para SQLite.
- Categoría de cada enlace.
- URL normalizada.
- Favoritos.
- Fecha de creación.

La eliminación de una categoría debe usar `DeleteBehavior.Cascade`.

## Arquitectura

Organiza la solución de forma mantenible:

```text
GestionEnlaces.sln
src/
  GestionEnlaces.Web/
tests/
  GestionEnlaces.Tests/
```

Dentro del proyecto web utiliza carpetas como:

- `Controllers`
- `Data`
- `Models`
- `DTOs`
- `Services`
- `Validation`
- `Views`
- `wwwroot`

Usa:

- Inyección de dependencias.
- Programación asíncrona con `async` y `await`.
- `CancellationToken` cuando corresponda.
- DTOs para la API; no expongas directamente las entidades.
- Validación de entrada en servidor.
- Servicios para búsqueda, importación, exportación y estadísticas.
- Consultas de solo lectura con `AsNoTracking()`.
- Migraciones de Entity Framework Core.
- Manejo centralizado de excepciones.
- Problem Details para errores HTTP.
- Logging estructurado.
- Protección CSRF en formularios y operaciones mutables.
- HTML codificado y prácticas seguras contra XSS.
- Ningún secreto dentro del repositorio.

## API REST

Implementa endpoints equivalentes a:

### Categorías

- `GET /api/categorias`
- `GET /api/categorias/{id}`
- `POST /api/categorias`
- `PUT /api/categorias/{id}`
- `DELETE /api/categorias/{id}`

### Enlaces

- `GET /api/enlaces`
- `GET /api/enlaces?categoriaId={id}`
- `GET /api/enlaces/{id}`
- `POST /api/enlaces`
- `PUT /api/enlaces/{id}`
- `DELETE /api/enlaces/{id}`
- `POST /api/enlaces/{id}/favorito`
- `POST /api/enlaces/{id}/click`

### Funciones adicionales

- `GET /api/estadisticas`
- `GET /api/buscar?q={texto}`
- `GET /api/favoritos`
- `GET /api/exportar`
- `POST /api/importar`

Usa correctamente los códigos HTTP:

- 200 para consultas y actualizaciones exitosas.
- 201 al crear.
- 204 cuando no sea necesario devolver contenido.
- 400 para datos inválidos.
- 404 cuando el recurso no exista.
- 409 para conflictos, como nombres duplicados.
- 500 únicamente para errores inesperados.

Mantén un formato JSON consistente. No devuelvas detalles internos, consultas SQL, rutas físicas ni stack traces al cliente.

## Interfaz

Crear estas vistas:

- `/`: tarjetas con las categorías.
- `/dashboard`: estadísticas, favoritos, enlaces recientes y populares.
- `/categoria/{id}`: enlaces pertenecientes a una categoría.
- Página 404 amigable.
- Página de error general.

Diseño visual:

- Tema oscuro elegante.
- Fondo oscuro con gradientes azules y morados.
- Tarjetas con efecto glass.
- Bordes y sombras luminosas sutiles.
- Diseño mobile-first y responsive.
- Navegación clara.
- Modales accesibles para crear y editar.
- Toasts para operaciones exitosas y errores.
- Indicadores de carga.
- Estados vacíos.
- Confirmación antes de eliminar.
- Navegación mediante teclado.
- Etiquetas ARIA y foco visible.
- Buen contraste de colores.
- Texto y mensajes en español.

Usa Tailwind CSS mediante un proceso de compilación apropiado para producción. Evita depender del CDN en la versión final.

## SQLite

Configura la conexión en `appsettings.json`:

```text
Data Source=Data/enlaces.db
```

La aplicación debe:

- Crear el directorio `Data` cuando no exista.
- Aplicar las migraciones pendientes durante el inicio en Development.
- Activar claves foráneas de SQLite.
- No incluir el archivo `.db` en Git.
- Incluir datos iniciales opcionales únicamente en Development.
- Funcionar correctamente en Windows, Linux y macOS.

## Pruebas

Incluye pruebas unitarias y de integración para:

- Crear, editar y eliminar categorías.
- Rechazar categorías duplicadas.
- Eliminación en cascada.
- Crear y editar enlaces.
- Normalización y validación de URL.
- Cambio de favorito.
- Registro de clics.
- Búsqueda.
- Estadísticas.
- Importación y exportación.
- Respuestas 400, 404 y 409.
- Persistencia con SQLite en memoria para pruebas de integración.

## Entregables

Genera:

- Todos los archivos del proyecto.
- Solución y proyectos `.sln` y `.csproj`.
- Migración inicial de Entity Framework Core.
- Código fuente completo, sin pseudocódigo.
- Pruebas automatizadas.
- `.gitignore`.
- `README.md` en español.
- Instrucciones para Windows, Linux y macOS.
- Configuración de Development y Production.
- Un archivo `appsettings.Example.json` si fuera necesario.
- Dockerfile opcional.
- Datos de demostración en Development.

El README debe explicar cómo ejecutar:

```powershell
dotnet restore
dotnet ef database update --project src/GestionEnlaces.Web
dotnet run --project src/GestionEnlaces.Web
dotnet test
```

## Forma de trabajo

1. Examina primero la aplicación existente para conservar sus funcionalidades y experiencia visual.
2. Presenta un resumen corto de la arquitectura propuesta.
3. Implementa la solución completa por etapas.
4. Después de cada etapa, compila y corrige los errores.
5. Ejecuta todas las migraciones y pruebas.
6. Verifica manualmente los flujos principales.
7. No declares terminado el trabajo mientras existan errores de compilación o pruebas fallidas.
8. No reemplaces funcionalidades existentes por marcadores, TODO o pseudocódigo.
9. Al terminar, proporciona:
   - Resumen de lo implementado.
   - Estructura final.
   - Decisiones técnicas importantes.
   - Comandos exactos de ejecución.
   - Resultado de compilación y pruebas.

## Criterios de aceptación

La tarea está terminada cuando:

- `dotnet build` finaliza sin errores.
- `dotnet test` finaliza correctamente.
- La base SQLite se crea mediante migraciones.
- Todos los CRUD funcionan.
- La búsqueda, favoritos, estadísticas, clics, importación y exportación funcionan.
- La interfaz es responsive y accesible.
- No existen errores visibles en la consola del navegador.
- El proyecto puede clonarse y ejecutarse siguiendo únicamente el README.

