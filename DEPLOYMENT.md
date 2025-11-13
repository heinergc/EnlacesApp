# Guía de Deployment - Enlaces App

Esta guía te ayudará a deployar tu aplicación de gestión de enlaces en Render.com (gratis).

## Opción 1: Deployment en Render.com (Recomendado)

Render.com ofrece un tier gratuito perfecto para esta aplicación.

### Paso 1: Preparar el repositorio

1. Asegúrate de que todos los archivos estén commiteados y pusheados a GitHub:
   ```bash
   git add .
   git commit -m "Preparar aplicación para deployment"
   git push origin <tu-rama>
   ```

### Paso 2: Crear cuenta en Render

1. Ve a [render.com](https://render.com)
2. Regístrate con tu cuenta de GitHub
3. Autoriza a Render para acceder a tus repositorios

### Paso 3: Crear un nuevo Web Service

1. En el dashboard de Render, haz clic en **"New +"**
2. Selecciona **"Web Service"**
3. Conecta tu repositorio de GitHub (heinergc/EnlacesApp)
4. Selecciona la rama que deseas deployar

### Paso 4: Configurar el servicio

Configura los siguientes parámetros:

- **Name**: `enlaces-app` (o el nombre que prefieras)
- **Environment**: `Python 3`
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn app:app`
- **Plan**: `Free`

### Paso 5: Variables de entorno (opcional)

Render generará automáticamente una SECRET_KEY, pero si quieres personalizarla:

1. En la sección **Environment Variables**, agrega:
   - `SECRET_KEY`: (genera una clave secreta fuerte)
   - `DATABASE_URL`: `sqlite:///enlaces.db` (ya configurado por defecto)

### Paso 6: Deploy

1. Haz clic en **"Create Web Service"**
2. Render comenzará a buildear y deployar tu aplicación
3. El proceso tomará unos minutos
4. Una vez completado, recibirás una URL como: `https://enlaces-app.onrender.com`

### Notas importantes sobre el tier gratuito de Render

- La aplicación se "dormirá" después de 15 minutos de inactividad
- El primer request después de dormir tomará ~30 segundos en despertar
- La base de datos SQLite se reiniciará cada vez que se redeploy (considera usar PostgreSQL para persistencia)

## Opción 2: Deployment en Railway.app

Railway es otra excelente opción con tier gratuito.

### Pasos rápidos:

1. Ve a [railway.app](https://railway.app)
2. Conecta con GitHub
3. Selecciona tu repositorio
4. Railway detectará automáticamente que es una app Flask
5. Deploy automático

## Opción 3: Deployment en PythonAnywhere

PythonAnywhere es específico para Python y muy fácil de usar.

### Pasos rápidos:

1. Crea una cuenta en [pythonanywhere.com](https://www.pythonanywhere.com)
2. Sube tu código o clona desde GitHub
3. Configura un Web App con Flask
4. Configura el WSGI file
5. Tu app estará disponible en: `tu-usuario.pythonanywhere.com`

## Opción 4: Deployment en Fly.io

Fly.io ofrece un tier gratuito generoso.

### Pasos:

1. Instala flyctl: `curl -L https://fly.io/install.sh | sh`
2. Login: `flyctl auth login`
3. Launch: `flyctl launch`
4. Deploy: `flyctl deploy`

## Base de datos en producción

Para esta aplicación usamos SQLite que es perfecto para desarrollo, pero tiene limitaciones:

- **SQLite en Render**: Los datos se perderán en cada redeploy
- **Solución recomendada**: Migrar a PostgreSQL (gratis en Render)

### Migrar a PostgreSQL:

1. En Render, crea un PostgreSQL database (Free tier)
2. Actualiza `requirements.txt`:
   ```
   psycopg2-binary==2.9.9
   ```
3. Actualiza la DATABASE_URL para usar PostgreSQL
4. Modifica el código para manejar las diferencias entre SQLite y PostgreSQL

## Troubleshooting

### Error: "Application failed to start"
- Verifica que `gunicorn` esté en `requirements.txt`
- Verifica que el comando start sea: `gunicorn app:app`

### Error: "Module not found"
- Verifica que todas las dependencias estén en `requirements.txt`
- Ejecuta localmente: `pip install -r requirements.txt`

### La aplicación no guarda datos
- SQLite en Render no persiste entre deploys
- Considera migrar a PostgreSQL

## Monitoreo

Una vez desplegada, puedes:
- Ver logs en tiempo real en el dashboard de Render
- Configurar alertas por email
- Monitorear uso de recursos

## Actualizar la aplicación

Para actualizar tu aplicación deployada:

```bash
git add .
git commit -m "Descripción de cambios"
git push origin <tu-rama>
```

Render automáticamente detectará los cambios y redesplegará.

## Soporte

Si tienes problemas:
- Revisa los logs en el dashboard de Render
- Consulta la documentación de Render: https://render.com/docs
- Abre un issue en el repositorio

---

¡Buena suerte con tu deployment! 🚀
