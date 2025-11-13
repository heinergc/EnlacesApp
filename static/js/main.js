/**
 * Funciones JavaScript Globales para la Aplicación de Gestión de Enlaces
 */

// ================================
// Sistema de Notificaciones Toast
// ================================

/**
 * Muestra una notificación toast al usuario
 * @param {string} mensaje - El mensaje a mostrar
 * @param {string} tipo - El tipo de notificación ('success', 'error', 'warning', 'info')
 */
function mostrarNotificacion(mensaje, tipo = 'info') {
    const toastElement = document.getElementById('notificationToast');
    const toastTitle = document.getElementById('toastTitle');
    const toastMessage = document.getElementById('toastMessage');
    const toastHeader = toastElement.querySelector('.toast-header');

    // Configurar el contenido
    toastMessage.textContent = mensaje;

    // Configurar el estilo según el tipo
    toastHeader.classList.remove('bg-success', 'bg-danger', 'bg-warning', 'bg-info', 'text-white');

    switch (tipo) {
        case 'success':
            toastTitle.innerHTML = '<i class="bi bi-check-circle-fill me-2"></i>Éxito';
            toastHeader.classList.add('bg-success', 'text-white');
            break;
        case 'error':
            toastTitle.innerHTML = '<i class="bi bi-exclamation-circle-fill me-2"></i>Error';
            toastHeader.classList.add('bg-danger', 'text-white');
            break;
        case 'warning':
            toastTitle.innerHTML = '<i class="bi bi-exclamation-triangle-fill me-2"></i>Advertencia';
            toastHeader.classList.add('bg-warning', 'text-white');
            break;
        case 'info':
        default:
            toastTitle.innerHTML = '<i class="bi bi-info-circle-fill me-2"></i>Información';
            toastHeader.classList.add('bg-info', 'text-white');
            break;
    }

    // Mostrar el toast
    const toast = new bootstrap.Toast(toastElement, {
        autohide: true,
        delay: 4000
    });
    toast.show();
}

// ================================
// Utilidades de Validación
// ================================

/**
 * Valida si una URL tiene el formato correcto
 * @param {string} url - La URL a validar
 * @returns {boolean} - True si la URL es válida
 */
function validarUrl(url) {
    try {
        new URL(url);
        return true;
    } catch (error) {
        return false;
    }
}

/**
 * Sanitiza un string para prevenir XSS
 * @param {string} str - El string a sanitizar
 * @returns {string} - El string sanitizado
 */
function sanitizeString(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

// ================================
// Utilidades de Formato
// ================================

/**
 * Formatea una fecha a un formato legible
 * @param {string} isoDate - Fecha en formato ISO
 * @returns {string} - Fecha formateada
 */
function formatearFecha(isoDate) {
    if (!isoDate) return 'N/A';

    const fecha = new Date(isoDate);
    const opciones = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };

    return fecha.toLocaleDateString('es-ES', opciones);
}

/**
 * Trunca un texto a una longitud específica
 * @param {string} texto - El texto a truncar
 * @param {number} longitud - La longitud máxima
 * @returns {string} - El texto truncado
 */
function truncarTexto(texto, longitud = 50) {
    if (texto.length <= longitud) return texto;
    return texto.substring(0, longitud) + '...';
}

// ================================
// Búsqueda de Google
// ================================

/**
 * Realiza una búsqueda en Google con el término ingresado
 */
function realizarBusquedaGoogle() {
    const input = document.getElementById('googleSearchInput');
    const searchTerm = input.value.trim();

    if (searchTerm === '') {
        mostrarNotificacion('Por favor ingresa un término de búsqueda', 'warning');
        input.focus();
        return;
    }

    // Codificar el término de búsqueda para URL
    const encodedSearch = encodeURIComponent(searchTerm);

    // Abrir Google en una nueva pestaña con el término de búsqueda
    window.open(`https://www.google.com/search?q=${encodedSearch}`, '_blank');

    // Limpiar el campo de búsqueda
    input.value = '';
}

// ================================
// Utilidades de Animación
// ================================

/**
 * Agrega una animación de fade-in a un elemento
 * @param {HTMLElement} elemento - El elemento a animar
 */
function animarFadeIn(elemento) {
    if (!elemento) return;
    elemento.classList.add('fade-in');
}

/**
 * Muestra un loader mientras se ejecuta una operación asíncrona
 * @param {boolean} mostrar - True para mostrar, false para ocultar
 */
function toggleLoader(mostrar) {
    const loader = document.getElementById('loader');
    if (loader) {
        loader.style.display = mostrar ? 'block' : 'none';
    }
}

// ================================
// Manejo de Errores API
// ================================

/**
 * Maneja errores de las llamadas a la API
 * @param {Error} error - El objeto de error
 * @param {string} accion - Descripción de la acción que falló
 */
function manejarErrorApi(error, accion = 'realizar la operación') {
    console.error(`Error al ${accion}:`, error);
    mostrarNotificacion(
        `No se pudo ${accion}. Por favor, intenta nuevamente.`,
        'error'
    );
}

// ================================
// Utilidades de DOM
// ================================

/**
 * Limpia el contenido de un elemento
 * @param {string} elementId - El ID del elemento
 */
function limpiarElemento(elementId) {
    const elemento = document.getElementById(elementId);
    if (elemento) {
        elemento.innerHTML = '';
    }
}

/**
 * Muestra u oculta un elemento por su ID
 * @param {string} elementId - El ID del elemento
 * @param {boolean} mostrar - True para mostrar, false para ocultar
 */
function toggleElemento(elementId, mostrar) {
    const elemento = document.getElementById(elementId);
    if (elemento) {
        elemento.style.display = mostrar ? 'block' : 'none';
    }
}

// ================================
// Utilidades de Fetch API
// ================================

/**
 * Realiza una petición GET a la API
 * @param {string} url - La URL del endpoint
 * @returns {Promise} - Promise con la respuesta
 */
async function apiGet(url) {
    try {
        const response = await fetch(url);
        return await response.json();
    } catch (error) {
        manejarErrorApi(error, 'obtener datos');
        throw error;
    }
}

/**
 * Realiza una petición POST a la API
 * @param {string} url - La URL del endpoint
 * @param {Object} data - Los datos a enviar
 * @returns {Promise} - Promise con la respuesta
 */
async function apiPost(url, data) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        return await response.json();
    } catch (error) {
        manejarErrorApi(error, 'enviar datos');
        throw error;
    }
}

/**
 * Realiza una petición PUT a la API
 * @param {string} url - La URL del endpoint
 * @param {Object} data - Los datos a actualizar
 * @returns {Promise} - Promise con la respuesta
 */
async function apiPut(url, data) {
    try {
        const response = await fetch(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        return await response.json();
    } catch (error) {
        manejarErrorApi(error, 'actualizar datos');
        throw error;
    }
}

/**
 * Realiza una petición DELETE a la API
 * @param {string} url - La URL del endpoint
 * @returns {Promise} - Promise con la respuesta
 */
async function apiDelete(url) {
    try {
        const response = await fetch(url, {
            method: 'DELETE'
        });
        return await response.json();
    } catch (error) {
        manejarErrorApi(error, 'eliminar datos');
        throw error;
    }
}

// ================================
// Inicialización
// ================================

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar todos los tooltips de Bootstrap
    const tooltipTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Inicializar todos los popovers de Bootstrap
    const popoverTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="popover"]')
    );
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Inicializar búsqueda de Google
    const googleSearchForm = document.getElementById('googleSearchForm');
    if (googleSearchForm) {
        googleSearchForm.addEventListener('submit', function(event) {
            event.preventDefault();
            realizarBusquedaGoogle();
        });
    }

    // Log de inicialización
    console.log('✅ Aplicación de Gestión de Enlaces inicializada');
});

// ================================
// Prevención de Eventos por Defecto en Enlaces del Menú
// ================================

document.addEventListener('click', function(event) {
    // Prevenir el comportamiento por defecto en enlaces con onclick
    if (event.target.closest('[onclick]') && event.target.tagName === 'A') {
        if (event.target.getAttribute('href') === '#') {
            event.preventDefault();
        }
    }
});

// ================================
// Manejo de Errores Global
// ================================

window.addEventListener('error', function(event) {
    console.error('Error global capturado:', event.error);
});

window.addEventListener('unhandledrejection', function(event) {
    console.error('Promise rechazada no manejada:', event.reason);
});

// ================================
// Exportar funciones para uso global
// ================================

window.AppUtils = {
    mostrarNotificacion,
    validarUrl,
    sanitizeString,
    formatearFecha,
    truncarTexto,
    animarFadeIn,
    toggleLoader,
    manejarErrorApi,
    limpiarElemento,
    toggleElemento,
    apiGet,
    apiPost,
    apiPut,
    apiDelete
};
