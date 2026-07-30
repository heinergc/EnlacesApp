# 🚀 Guía de Instalación Rápida - Windows

## ⚡ Método Rápido (2 Pasos)

### Paso 1: Instalar Dependencias
```cmd
install.bat
```

### Paso 2: Ejecutar Aplicación
```cmd
start.bat
```

### ¡Listo! Abre tu navegador:
- http://localhost:5000
- http://localhost:5000/dashboard

---

## 🔧 Si Tienes Errores

### Error: "Python no está instalado"

**Solución:**
1. Descarga Python desde: https://www.python.org/downloads/
2. Durante la instalación:
   - ✅ Marca: "Add Python to PATH"
   - ✅ Marca: "pip"
   - ✅ Usa: "Install for all users"
3. Reinicia CMD
4. Ejecuta de nuevo: `install.bat`

---

### Error: "pip no disponible"

**Solución 1 - Reinstalar Python:**
1. Panel de Control → Desinstalar Python
2. Descarga versión más reciente
3. Instala marcando todas las opciones
4. Ejecuta: `install.bat`

**Solución 2 - Instalar pip manualmente:**
```cmd
python -m ensurepip --upgrade
python -m pip install --upgrade pip
install.bat
```

---

### Error: "No se pudo crear entorno virtual"

**No te preocupes - Los nuevos scripts NO usan entorno virtual**

Simplemente ejecuta:
```cmd
install.bat
start.bat
```

---

## 📂 Archivos de Ejecución

| Archivo | Descripción |
|---------|-------------|
| `install.bat` | Instala dependencias (solo primera vez) |
| `start.bat` | Inicia la aplicación |
| `run.bat` | Método antiguo (con venv, puede fallar) |

**Recomendado: Usa `install.bat` y `start.bat`**

---

## ✅ Verificar que Python Está Bien Instalado

Abre CMD y ejecuta:
```cmd
python --version
python -m pip --version
```

Deberías ver algo como:
```
Python 3.11.5
pip 23.2.1
```

Si ves esto, todo está bien instalado.

---

## 🎯 Resumen de Comandos

```cmd
# Primera vez:
cd /d E:\APLICACIONES\ENLACES
install.bat

# Cada vez que quieras ejecutar:
start.bat

# Abrir en navegador:
http://localhost:5000
http://localhost:5000/dashboard
```

---

## 🆘 Soporte

Si sigues teniendo problemas, verifica:
1. ✅ Python 3.8+ instalado
2. ✅ Python en PATH (escribe `python` en CMD)
3. ✅ pip instalado (`python -m pip --version`)
4. ✅ Ejecutaste `install.bat` primero
5. ✅ Estás en la carpeta correcta

---

## 🎉 Una Vez Funcionando

Tendrás acceso a:
- ✅ Gestión de Enlaces y Categorías
- ✅ Dashboard con Estadísticas
- ✅ Búsqueda Global
- ✅ Sistema de Favoritos
- ✅ Importar/Exportar datos
- ✅ Analítica de clicks
- ✅ Tutorial del Método Simplex

**¡Disfruta tu aplicación!** 🚀
