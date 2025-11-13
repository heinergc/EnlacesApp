# Configuración de Autenticación con Google OAuth

Esta guía te ayudará a configurar la autenticación con Google OAuth para tu aplicación de gestión de enlaces.

## ¿Por qué Google OAuth?

La aplicación ahora utiliza autenticación con Google OAuth para:
- **Seguridad**: Cada usuario solo puede ver y gestionar sus propios enlaces
- **Privacidad**: Los datos están completamente aislados por usuario
- **Facilidad**: Login con un solo clic usando tu cuenta de Google
- **Sin contraseñas**: No necesitas crear ni recordar contraseñas adicionales

## Configuración Paso a Paso

### 1. Crear Proyecto en Google Cloud Console

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto:
   - Click en el selector de proyectos (parte superior)
   - Click en "Nuevo Proyecto"
   - Nombre: "Enlaces App" (o el que prefieras)
   - Click en "Crear"

### 2. Habilitar la API de Google

1. En el menú lateral, ve a "APIs y servicios" → "Biblioteca"
2. Busca "Google+ API" o "Google Identity"
3. Click en la API y luego en "Habilitar"

### 3. Configurar Pantalla de Consentimiento

1. Ve a "APIs y servicios" → "Pantalla de consentimiento de OAuth"
2. Selecciona "Externo" (para permitir cualquier cuenta de Google)
3. Click en "Crear"
4. Completa el formulario:
   - **Nombre de la aplicación**: Enlaces App
   - **Correo de asistencia al usuario**: tu-email@gmail.com
   - **Logo** (opcional): Puedes dejarlo en blanco
   - **Dominios autorizados**:
     - `localhost` (para desarrollo)
     - `tu-app.onrender.com` (para producción)
   - **Correo de contacto del desarrollador**: tu-email@gmail.com
5. Click en "Guardar y continuar"
6. En "Scopes", click en "Guardar y continuar" (no necesitamos scopes adicionales)
7. En "Usuarios de prueba", agrega tu correo y otros correos que quieras permitir
8. Click en "Guardar y continuar"

### 4. Crear Credenciales OAuth

1. Ve a "APIs y servicios" → "Credenciales"
2. Click en "+ CREAR CREDENCIALES" → "ID de cliente de OAuth"
3. Selecciona "Aplicación web"
4. Configura:
   - **Nombre**: Enlaces App Web Client
   - **Orígenes autorizados de JavaScript**:
     - `http://localhost:5000` (desarrollo)
     - `https://tu-app.onrender.com` (producción)
   - **URIs de redirección autorizados**:
     - `http://localhost:5000/authorize` (desarrollo)
     - `https://tu-app.onrender.com/authorize` (producción)
5. Click en "Crear"
6. **IMPORTANTE**: Guarda el "Client ID" y el "Client Secret" que aparecen

### 5. Configurar Variables de Entorno

#### Para Desarrollo Local:

1. Crea un archivo `.env` en la raíz del proyecto (copia de `.env.example`):
   ```bash
   cp .env.example .env
   ```

2. Edita el archivo `.env` y agrega tus credenciales:
   ```bash
   SECRET_KEY=genera-una-clave-secreta-aleatoria-aqui
   GOOGLE_CLIENT_ID=tu-client-id.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=tu-client-secret
   ```

3. Para generar una SECRET_KEY segura, puedes usar:
   ```python
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

#### Para Producción en Render:

1. Ve a tu servicio en [Render Dashboard](https://dashboard.render.com)
2. Ve a "Environment" → "Environment Variables"
3. Agrega las siguientes variables:
   - `GOOGLE_CLIENT_ID`: tu-client-id.apps.googleusercontent.com
   - `GOOGLE_CLIENT_SECRET`: tu-client-secret
   - `SECRET_KEY`: (Render puede generarla automáticamente o usa la que generaste)
4. Click en "Save Changes"
5. Render redesplegará automáticamente tu aplicación

### 6. Actualizar URLs de Redirección

**IMPORTANTE**: Cuando despliegues en Render, debes actualizar las URLs de redirección:

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Ve a "Credenciales" → Click en tu "ID de cliente de OAuth"
3. En "URIs de redirección autorizados", asegúrate de tener:
   - `http://localhost:5000/authorize` (desarrollo)
   - `https://TU-APP.onrender.com/authorize` (reemplaza TU-APP con tu URL real)
4. Click en "Guardar"

## Probar la Autenticación

### En Desarrollo Local:

1. Asegúrate de tener el archivo `.env` configurado
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecuta la aplicación:
   ```bash
   python app.py
   ```
4. Abre http://localhost:5000
5. Click en "Iniciar con Google"
6. Selecciona tu cuenta de Google
7. Autoriza la aplicación
8. Deberías ser redirigido de vuelta a la app ya autenticado

### En Producción (Render):

1. Asegúrate de haber configurado las variables de entorno en Render
2. Actualiza las URLs de redirección en Google Cloud Console
3. Despliega tu aplicación
4. Visita tu URL de Render
5. Click en "Iniciar con Google"
6. Completa el flujo de OAuth

## Solución de Problemas

### Error: "redirect_uri_mismatch"

**Causa**: La URL de redirección no coincide con las configuradas en Google Cloud Console.

**Solución**:
1. Verifica que la URL en el error coincida exactamente con la que agregaste en Google Cloud Console
2. Asegúrate de incluir `http://` o `https://`
3. No olvides el `/authorize` al final
4. Los espacios y mayúsculas/minúsculas importan

### Error: "invalid_client"

**Causa**: El Client ID o Client Secret son incorrectos.

**Solución**:
1. Verifica que copiaste correctamente el Client ID y Secret
2. No debe haber espacios al inicio o final
3. Regenera las credenciales si es necesario

### Error: "access_denied"

**Causa**: El usuario canceló la autorización o la app no tiene permisos.

**Solución**:
1. Asegúrate de que el usuario está en la lista de "Usuarios de prueba" si la app no está publicada
2. Intenta nuevamente el proceso de login

### La aplicación no guarda la sesión

**Causa**: Falta SECRET_KEY o no está configurada correctamente.

**Solución**:
1. Asegúrate de que SECRET_KEY esté configurada en `.env` (local) o en Render (producción)
2. La SECRET_KEY debe ser la misma entre reinicios de la aplicación

### No puedo ver los enlaces de otro usuario

**Esto es correcto**: Cada usuario solo puede ver sus propios enlaces. Es por diseño de seguridad.

## Características de Seguridad

La implementación incluye:

✅ **Aislamiento de datos**: Cada usuario solo ve sus propios enlaces
✅ **Validación de sesión**: Todas las operaciones requieren autenticación
✅ **Tokens seguros**: Uso de OAuth 2.0 con Google
✅ **HTTPS en producción**: Las credenciales se transmiten de forma segura
✅ **Secret Key**: Sesiones firmadas criptográficamente

## Migración de Datos Existentes

Si ya tenías datos antes de implementar autenticación:

**IMPORTANTE**: Los datos antiguos no tienen `usuario_id`, por lo que no serán accesibles después de la migración. Considera:

1. Exportar los datos importantes antes de actualizar
2. Eliminar la base de datos antigua (`rm enlaces.db`)
3. Dejar que la aplicación cree una nueva base de datos
4. Crear los datos nuevamente con autenticación

## Recursos Adicionales

- [Documentación de Google OAuth](https://developers.google.com/identity/protocols/oauth2)
- [Google Cloud Console](https://console.cloud.google.com/)
- [Documentación de Flask-Login](https://flask-login.readthedocs.io/)
- [Documentación de Authlib](https://docs.authlib.org/en/latest/)

## Soporte

Si tienes problemas:
1. Revisa los logs de la aplicación
2. Verifica que las variables de entorno estén correctamente configuradas
3. Confirma que las URLs de redirección coincidan exactamente
4. Abre un issue en el repositorio de GitHub

---

¡Ahora tu aplicación está protegida con autenticación de Google! 🔐
