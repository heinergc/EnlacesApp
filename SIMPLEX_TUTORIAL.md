# 📊 Tutorial Interactivo del Método Simplex

## Descripción

Aplicación web educativa e interactiva diseñada para enseñar el **Método Simplex** paso a paso a estudiantes de Investigación de Operaciones en Ingeniería.

## Características

### 🎓 Contenido Educativo

1. **Teoría Completa**
   - ¿Qué es el Método Simplex?
   - Componentes de Programación Lineal
   - Forma estándar
   - Variables de holgura

2. **Pasos del Algoritmo**
   - Explicación detallada de cada paso
   - Identificación de columna pivote
   - Identificación de fila pivote
   - Operaciones de pivoteo
   - Criterios de optimalidad

3. **Ejemplo Interactivo**
   - Problema real resuelto paso a paso
   - Visualización de tablas Simplex
   - Navegación entre iteraciones
   - Destacado de elementos pivote
   - Explicaciones contextuales

4. **Ejercicios de Práctica**
   - Problemas de producción
   - Problemas de dieta
   - Problemas de transporte
   - Recursos adicionales

### ✨ Características Interactivas

- **Navegación paso a paso**: Avanza y retrocede entre las iteraciones
- **Visualización dinámica**: Tablas Simplex con colores y animaciones
- **Destacado visual**: Elementos pivote, filas y columnas resaltadas
- **Indicadores de progreso**: Seguimiento visual del algoritmo
- **Explicaciones contextuales**: Cada paso incluye explicación detallada
- **Diseño responsivo**: Funciona en móviles, tablets y escritorio

### 🎨 Diseño

- Interfaz moderna y atractiva
- Sistema de pestañas para organizar el contenido
- Animaciones suaves
- Código de colores intuitivo
- Tipografía matemática apropiada

## Cómo Acceder

### Desde la Aplicación Web

1. Inicia la aplicación de Gestión de Enlaces
2. Ve a la categoría **"Educación"**
3. Haz clic en **"📊 Tutorial Método Simplex"**

### Acceso Directo

Cuando el servidor esté corriendo, visita:
```
http://localhost:5000/simplex
```

## Contenido del Tutorial

### Sección 1: Teoría
- Introducción al Método Simplex
- Programación Lineal
- Forma estándar
- Variables de holgura y artificiales

### Sección 2: Algoritmo
- 6 pasos detallados del método
- Criterios de optimalidad
- Reglas de pivoteo
- Interpretación de resultados

### Sección 3: Ejemplo Interactivo
**Problema:**
```
Maximizar: Z = 3x₁ + 2x₂

Sujeto a:
2x₁ + x₂ ≤ 18
2x₁ + 3x₂ ≤ 42
3x₁ + x₂ ≤ 24
x₁, x₂ ≥ 0
```

**Solución óptima:**
- x₁ = 6
- x₂ = 6
- Z = 30

### Sección 4: Práctica
- 3 ejercicios propuestos
- Diferentes tipos de problemas
- Recursos adicionales
- Consejos prácticos

## Tecnologías Utilizadas

- **HTML5**: Estructura semántica
- **CSS3**: Diseño responsivo y animaciones
- **JavaScript**: Interactividad y navegación
- **Bootstrap Icons**: Iconografía

## Estructura del Código

```javascript
// Estado del ejemplo
let currentStep = 0;
const maxSteps = 3;

// Datos de las tablas
const tableaux = [
    // Tabla inicial
    // Iteración 1
    // Iteración 2
    // Solución óptima
];

// Funciones principales
- showTab(tabName)          // Cambiar entre pestañas
- renderTableau(stepIndex)  // Renderizar tabla
- nextStep()                // Avanzar paso
- previousStep()            // Retroceder paso
- resetExample()            // Reiniciar ejemplo
```

## Características Pedagógicas

### Aprendizaje Visual
- Colores diferentes para pivote, fila y columna
- Animaciones que llaman la atención
- Indicadores de progreso claros

### Aprendizaje Progresivo
- De la teoría a la práctica
- Explicaciones antes de cada acción
- Ejercicios de complejidad creciente

### Aprendizaje Interactivo
- Control del ritmo de aprendizaje
- Posibilidad de repetir pasos
- Verificación visual de resultados

## Uso Educativo

### Para Estudiantes
1. Lee primero la sección de **Teoría**
2. Estudia los **Pasos del Método**
3. Sigue el **Ejemplo Interactivo** paso a paso
4. Practica con los ejercicios propuestos
5. Verifica tus resultados con software

### Para Profesores
- Herramienta de apoyo para clases
- Recurso para explicar conceptos
- Ejercicios para asignar a estudiantes
- Referencia rápida del algoritmo

## Extensiones Futuras

Posibles mejoras:
- [ ] Calculadora Simplex personalizada
- [ ] Más ejemplos resueltos
- [ ] Método de las Dos Fases
- [ ] Análisis de sensibilidad
- [ ] Exportar resultados a PDF
- [ ] Problema de Minimización
- [ ] Variables artificiales
- [ ] Problemas degenerados

## Referencias

- Hamdy Taha - "Investigación de Operaciones"
- Hillier & Lieberman - "Introduction to Operations Research"
- George Dantzig - Creador del Método Simplex (1947)

## Licencia

Material educativo de libre uso para fines académicos.

---

**Desarrollado para facilitar el aprendizaje de Investigación de Operaciones en Ingeniería** 🎓
