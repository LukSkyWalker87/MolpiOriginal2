// Script para cargar productos podotáctiles dinámicamente desde la API
document.addEventListener('DOMContentLoaded', function() {
    cargarProductosPodotactiles();
});

async function cargarProductosPodotactiles() {
    try {
        console.log('Cargando productos podotáctiles desde API...');
        
        // Cargar productos desde la API
        const response = await fetch('/productos');
        const productos = await response.json();
        
        // Obtener todos los productos podotáctiles (activos e inactivos)
        const todosPodotactiles = productos.filter(p => p.categoria === 'Podotáctiles');
        
        // Filtrar solo productos podotáctiles activos
        const podotactilesActivos = todosPodotactiles.filter(p => p.activo === 1);
        
        console.log('Productos podotáctiles encontrados:', todosPodotactiles);
        console.log('Productos podotáctiles activos:', podotactilesActivos);
        
        // Actualizar contenido basado en productos activos e inactivos
        actualizarContenidoPodotactiles(podotactilesActivos, todosPodotactiles);
        
    } catch (error) {
        console.error('Error cargando productos podotáctiles:', error);
        console.log('Manteniendo contenido estático debido al error');
    }
}

function actualizarContenidoPodotactiles(productosActivos, todosProductos) {
    // Mapear productos activos por nombre para fácil acceso
    const productosActivosMap = {};
    productosActivos.forEach(producto => {
        if (producto.nombre.includes('Círculos')) {
            productosActivosMap.circulos = producto;
        } else if (producto.nombre.includes('Barras')) {
            productosActivosMap.barras = producto;
        } else if (producto.nombre.includes('Discapacitados')) {
            productosActivosMap.discapacitados = producto;
        }
    });
    
    // Mapear todos los productos para verificar cuáles existen pero están inactivos
    const todosProductosMap = {};
    todosProductos.forEach(producto => {
        if (producto.nombre.includes('Círculos')) {
            todosProductosMap.circulos = producto;
        } else if (producto.nombre.includes('Barras')) {
            todosProductosMap.barras = producto;
        } else if (producto.nombre.includes('Discapacitados')) {
            todosProductosMap.discapacitados = producto;
        }
    });
    
    // Actualizar o ocultar sección de círculos
    if (productosActivosMap.circulos) {
        mostrarSeccionCirculos(productosActivosMap.circulos);
    } else if (todosProductosMap.circulos) {
        ocultarSeccionCirculos();
    }
    
    // Actualizar o ocultar sección de barras
    if (productosActivosMap.barras) {
        mostrarSeccionBarras(productosActivosMap.barras);
    } else if (todosProductosMap.barras) {
        ocultarSeccionBarras();
    }
    
    // Actualizar o ocultar sección de discapacitados
    if (productosActivosMap.discapacitados) {
        mostrarSeccionDiscapacitados(productosActivosMap.discapacitados);
    } else if (todosProductosMap.discapacitados) {
        ocultarSeccionDiscapacitados();
    }
}

function mostrarSeccionCirculos(producto) {
    // Encontrar la sección completa de círculos
    const elementosSeccion = encontrarSeccionPorTexto('Con Círculos');
    if (elementosSeccion && elementosSeccion.length > 0) {
        elementosSeccion.forEach(elemento => {
            elemento.style.display = 'block';
        });
        console.log('Sección de círculos mostrada');
    }
    
    // Actualizar imágenes
    const imgMolde = document.querySelector('img[src*="circulos_ciegos_molde"]');
    const imgMosaico = document.querySelector('img[src*="circulos_ciegos_mosaico"]');
    
    if (imgMolde && producto.imagen_url) {
        imgMolde.src = producto.imagen_url;
        imgMolde.alt = producto.nombre + ' - Molde';
    }
    
    if (imgMosaico && producto.imagen_mosaico_url) {
        imgMosaico.src = producto.imagen_mosaico_url;
        imgMosaico.alt = producto.nombre + ' - Mosaico';
    }
    
    // Actualizar descripción
    const paragraphs = document.querySelectorAll('p');
    paragraphs.forEach(p => {
        if (p.textContent.includes('pisos podotáctiles de advertencia')) {
            // Mantener el formato con negritas
            const strongText = p.querySelector('strong');
            if (strongText && producto.descripcion) {
                p.innerHTML = `<strong>Los pisos podotáctiles de advertencia</strong> ${producto.descripcion}`;
            }
        }
    });
}

function ocultarSeccionCirculos() {
    const elementosSeccion = encontrarSeccionPorTexto('Con Círculos');
    if (elementosSeccion && elementosSeccion.length > 0) {
        elementosSeccion.forEach(elemento => {
            elemento.style.display = 'none';
        });
        console.log('Sección de círculos ocultada (producto inactivo)');
    }
}

function mostrarSeccionBarras(producto) {
    // Encontrar la sección completa de barras
    const elementosSeccion = encontrarSeccionPorTexto('Con Barras');
    if (elementosSeccion && elementosSeccion.length > 0) {
        elementosSeccion.forEach(elemento => {
            elemento.style.display = 'block';
        });
        console.log('Sección de barras mostrada');
    }
    
    // Actualizar imágenes
    const imgMolde = document.querySelector('img[src*="barras_molde"]');
    const imgMosaico = document.querySelector('img[src*="barras_mosaico"]');
    
    if (imgMolde && producto.imagen_url) {
        imgMolde.src = producto.imagen_url;
        imgMolde.alt = producto.nombre + ' - Molde';
    }
    
    if (imgMosaico && producto.imagen_mosaico_url) {
        imgMosaico.src = producto.imagen_mosaico_url;
        imgMosaico.alt = producto.nombre + ' - Mosaico';
    }
    
    // Actualizar descripción
    const paragraphs = document.querySelectorAll('p');
    paragraphs.forEach(p => {
        if (p.textContent.includes('pisos podotáctiles de guia') || 
            p.textContent.includes('baldozas de barras')) {
            // Mantener el formato con negritas
            const strongText = p.querySelector('strong');
            if (strongText && producto.descripcion) {
                p.innerHTML = `<strong>Los pisos podotáctiles de guía o baldozas de barras</strong> ${producto.descripcion}`;
            }
        }
    });
}

function ocultarSeccionBarras() {
    const elementosSeccion = encontrarSeccionPorTexto('Con Barras');
    if (elementosSeccion && elementosSeccion.length > 0) {
        elementosSeccion.forEach(elemento => {
            elemento.style.display = 'none';
        });
        console.log('Sección de barras ocultada (producto inactivo)');
    }
}
                p.textContent = producto.descripcion;
            }
        }
    });
}

function mostrarSeccionDiscapacitados(producto) {
    // Encontrar la sección completa de discapacitados
    const elementosSeccion = encontrarSeccionPorTexto('Señal Discapacitados');
    if (elementosSeccion && elementosSeccion.length > 0) {
        elementosSeccion.forEach(elemento => {
            elemento.style.display = 'block';
        });
        console.log('Sección de discapacitados mostrada');
    }
    
    // Buscar y actualizar imágenes de señal de discapacitados
    const imgMolde = document.querySelector('img[src*="discapacitado_molde"]');
    const imgMosaico = document.querySelector('img[src*="discapacitado_mosaico"]');
    
    if (imgMolde && producto.imagen_url) {
        imgMolde.src = producto.imagen_url;
        imgMolde.alt = producto.nombre + ' - Molde';
    }
    
    if (imgMosaico && producto.imagen_mosaico_url) {
        imgMosaico.src = producto.imagen_mosaico_url;
        imgMosaico.alt = producto.nombre + ' - Mosaico';
    }
    
    // Actualizar descripción
    const paragraphs = document.querySelectorAll('p');
    paragraphs.forEach(p => {
        if (p.textContent.includes('lugares reservados para accesibilidad') ||
            p.textContent.includes('comunicación hacia las personas videntes')) {
            if (producto.descripcion) {
                p.textContent = producto.descripcion;
            }
        }
    });
}

function ocultarSeccionDiscapacitados() {
    const elementosSeccion = encontrarSeccionPorTexto('Señal Discapacitados');
    if (elementosSeccion && elementosSeccion.length > 0) {
        elementosSeccion.forEach(elemento => {
            elemento.style.display = 'none';
        });
        console.log('Sección de discapacitados ocultada (producto inactivo)');
    }
}

// Función auxiliar para buscar elementos por contenido de texto
function encontrarElementoPorTexto(selector, texto) {
    const elementos = document.querySelectorAll(selector);
    for (let elemento of elementos) {
        if (elemento.textContent.includes(texto)) {
            return elemento;
        }
    }
    return null;
}

// Función auxiliar para encontrar secciones completas por texto de título
function encontrarSeccionPorTexto(textoTitulo) {
    // Buscar por h4 que contenga el título
    const titulo = encontrarElementoPorTexto('h4', textoTitulo);
    if (!titulo) {
        console.log(`No se encontró título: ${textoTitulo}`);
        return null;
    }
    
    // El título está en un div col-md-5, necesitamos encontrar el grupo completo
    const colTexto = titulo.closest('.col-md-5');
    if (!colTexto) {
        console.log(`No se encontró col-md-5 para: ${textoTitulo}`);
        return null;
    }
    
    // Buscar los elementos hermanos: col-md-4 (imágenes) y col-md-1 (espaciador)
    const container = colTexto.parentElement;
    let elementos = [];
    
    // Buscar hacia atrás para encontrar el col-md-4 (imágenes) y col-md-1 correspondientes
    let elementoAnterior = colTexto.previousElementSibling;
    while (elementoAnterior && elementos.length < 2) {
        if (elementoAnterior.classList.contains('col-md-1') || 
            elementoAnterior.classList.contains('col-md-4')) {
            elementos.unshift(elementoAnterior);
        }
        elementoAnterior = elementoAnterior.previousElementSibling;
    }
    
    // Agregar el elemento actual (col-md-5)
    elementos.push(colTexto);
    
    // Buscar el hr siguiente si existe
    let siguienteElemento = colTexto.nextElementSibling;
    if (siguienteElemento && siguienteElemento.classList.contains('col-md-12')) {
        const hr = siguienteElemento.querySelector('hr');
        if (hr) {
            elementos.push(siguienteElemento);
        }
    }
    
    console.log(`Encontrados ${elementos.length} elementos para sección: ${textoTitulo}`);
    return elementos;
}

// Log para debug
console.log('Script podotactiles-dinamico.js cargado');
