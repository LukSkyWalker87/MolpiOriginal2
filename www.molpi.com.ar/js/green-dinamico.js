// Script para cargar productos Green dinámicamente desde la API
function cargarProductosGreen() {
    console.log('🟢 Cargando productos Green desde la API...');
    
    fetch('/productos')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(productos => {
            console.log('📦 Productos recibidos:', productos.length);
            
            // Filtrar solo productos Green y activos
            const productosGreen = productos.filter(producto => 
                producto.categoria === 'Green' && producto.activo === 1
            );
            
            console.log('🟢 Productos Green encontrados:', productosGreen.length);
            
            // Renderizar productos con el formato original
            renderizarProductosGreenOriginal(productosGreen);
        })
        .catch(error => {
            console.error('❌ Error al cargar productos Green:', error);
            document.getElementById('productos-green-container').innerHTML = `
                <div class="col-md-12">
                    <div class="alert alert-warning">
                        <h4>Error al cargar productos</h4>
                        <p>No se pudieron cargar los productos Green. Por favor, intente más tarde.</p>
                    </div>
                </div>
            `;
        });
}

function renderizarProductosGreenOriginal(productos) {
    const container = document.getElementById('productos-green-container');
    
    if (!container) {
        console.error('❌ No se encontró el contenedor productos-green-container');
        return;
    }
    
    if (productos.length === 0) {
        container.innerHTML = `
            <div class="col-md-12">
                <div class="alert alert-info">
                    <h4>No hay productos disponibles</h4>
                    <p>No se encontraron productos Green activos en este momento.</p>
                </div>
            </div>
        `;
        return;
    }
    
    let html = '';
    
    // Orden específico de productos Green
    const ordenProductos = [
        'Green Rombos',
        'Círculos Green', 
        'Green Rectos',
        'Adoquín Individual',
        'Intertrabado'
    ];
    
    // Reordenar productos según el orden especificado
    const productosOrdenados = [];
    ordenProductos.forEach(nombreProducto => {
        const producto = productos.find(p => p.nombre === nombreProducto);
        if (producto) {
            productosOrdenados.push(producto);
        }
    });
    
    // Agregar cualquier producto Green que no esté en la lista específica
    productos.forEach(producto => {
        if (!ordenProductos.includes(producto.nombre)) {
            productosOrdenados.push(producto);
        }
    });
    
    productosOrdenados.forEach((producto, index) => {
        // Imagen de molde (usar imagen principal)
        const imagenMolde = producto.imagen_url || '';
        
        // Imagen de mosaico
        const imagenMosaico = producto.imagen_mosaico_url || '';
        
        // Generar descripción específica según el producto
        let descripcion = '';
        let tipoProducto = '';
        
        switch(producto.nombre) {
            case 'Green Rombos':
                tipoProducto = 'Romboidal.';
                descripcion = 'Aptos para entradas vehiculares o peatonales, dando un aspecto muy agradable y confortable entre espacio verde y el cemento gris.<br>- Medidas del producto final: 35 x 35 x 6 cm.';
                break;
            case 'Círculos Green':
                tipoProducto = 'Circular.';
                descripcion = 'Aptos para entradas vehiculares o peatonales, dando un aspecto muy agradable y confortable entre espacio verde y el cemento gris.<br>- Medidas del producto final: 35 x 35 x 6 cm.';
                break;
            case 'Green Rectos':
                tipoProducto = 'Numeral.';
                descripcion = 'Aptos para entradas vehiculares o peatonales, dando un aspecto muy agradable y confortable entre espacio verde y el cemento gris.<br>- Medidas del producto final: 35 x 35 x 6 cm.';
                break;
            case 'Adoquín Individual':
                tipoProducto = 'Individuales.';
                descripcion = 'Se pueden lograr caminos únicos, con libertad de diseño, gracias a su carácter individual.<br>Aptos para tránsito liviano o paseos peatonales.<br>- Medidas del producto final: 10 x 10 x 6 cm.<br>- Cada molde contiene 9 cavidades.';
                break;
            case 'Intertrabado':
                tipoProducto = 'Individuales.';
                descripcion = 'Su diseño encastrable aporta mayor firmeza y admite diferentes patrones en la colocación.<br>Aptos para tránsito liviano o paseos peatonales.<br>- Medidas del producto final: 20 x 10 x 6 cm.<br>- Cada molde contiene 4 cavidades.<br>- 50 unidades por m2.';
                break;
            default:
                tipoProducto = '';
                descripcion = producto.descripcion || 'Molde especializado para la línea Green. Ideal para jardines y exteriores con un diseño funcional y estético.';
        }
        
        // Agregar efecto de animación con delay escalonado
        const delay = index * 200; // 200ms de delay entre cada producto
        
        html += `
            <div class="col-md-4 producto-animate" data-delay="${delay}">
                ${imagenMolde ? `
                <img src="${imagenMolde}" 
                     data-appear-animation="fadeInLeft" 
                     data-appear-animation-delay="0" 
                     data-plugin-options="{'accY': 10}" 
                     alt="${producto.nombre}" 
                     class="custom-product-image-pos-1 _relative img-responsive producto-imagen" 
                     data-delay="${delay + 100}" />
                ` : ''}
                
                ${imagenMosaico ? `
                <img src="${imagenMosaico}" 
                     data-appear-animation="fadeInLeft" 
                     data-appear-animation-delay="200" 
                     data-plugin-options="{'accY': 10}" 
                     alt="${producto.nombre} - Mosaico" 
                     class="custom-product-image-pos-1 _absolute img-responsive producto-imagen" 
                     data-delay="${delay + 200}" />
                ` : ''}
            </div>
            <div class="col-md-1">
            </div>
            <div class="col-md-5 producto-animate" data-delay="${delay}">
                <h4 class="mb-xl mt-xlg producto-titulo" data-delay="${delay + 50}">${producto.nombre}</h4>
                <div class="divider divider-primary divider-small mb-xl producto-titulo" data-delay="${delay + 100}"> 
                    <hr>
                </div>
                <h4 class="heading-primary">Especificaciones:</h4>
                <p><strong>${tipoProducto}</strong> ${descripcion}</p>
            </div>
            <div class="col-md-12">
                <hr>
            </div>
        `;
    });
    
    container.innerHTML = html;
    
    // Activar animaciones personalizadas después de renderizar
    setTimeout(() => {
        activarAnimacionesGreen();
    }, 100);
    
    console.log('✅ Productos Green renderizados exitosamente con formato original');
}

function activarAnimacionesGreen() {
    // Obtener todos los elementos que necesitan animación
    const productosAnimate = document.querySelectorAll('.producto-animate');
    const titulosAnimate = document.querySelectorAll('.producto-titulo');
    const imagenesAnimate = document.querySelectorAll('.producto-imagen');
    
    // Animar productos
    productosAnimate.forEach(elemento => {
        const delay = parseInt(elemento.dataset.delay) || 0;
        setTimeout(() => {
            elemento.classList.add('show');
        }, delay);
    });
    
    // Animar títulos
    titulosAnimate.forEach(elemento => {
        const delay = parseInt(elemento.dataset.delay) || 0;
        setTimeout(() => {
            elemento.classList.add('show');
        }, delay);
    });
    
    // Animar imágenes
    imagenesAnimate.forEach(elemento => {
        const delay = parseInt(elemento.dataset.delay) || 0;
        setTimeout(() => {
            elemento.classList.add('show');
        }, delay);
    });
}

// Cargar productos cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 DOM cargado, inicializando carga de productos Green...');
    cargarProductosGreen();
});

// También cargar cuando la ventana esté completamente cargada (fallback)
window.addEventListener('load', function() {
    // Solo cargar si no se cargó antes
    const container = document.getElementById('productos-green-container');
    if (container && container.innerHTML.trim() === '') {
        console.log('🔄 Fallback: cargando productos Green...');
        cargarProductosGreen();
    }
});
