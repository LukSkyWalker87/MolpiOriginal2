// Script para cargar productos Listones dinámicamente desde la API, con animaciones y formato igual a Green
function cargarProductosListones() {
    console.log('🟫 Cargando productos Listones desde la API...');
    fetch('/api/productos?incluir_inactivos=false')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const productos = Array.isArray(data) ? data : data.productos;
            // Filtro tolerante
            const productosListones = productos.filter(producto => {
                const cat = (producto.categoria || '').toString().trim().toLowerCase();
                const esListon = cat === 'listones';
                const activo = Number(producto.activo) === 1;
                return esListon && activo;
            });
            renderizarProductosListones(productosListones);
        })
        .catch(error => {
            console.error('❌ Error al cargar productos Listones:', error);
            document.getElementById('productos-listones-container').innerHTML = `
                <div class="col-md-12">
                    <div class="alert alert-warning">
                        <h4>Error al cargar productos</h4>
                        <p>No se pudieron cargar los productos Listones. Por favor, intente más tarde.</p>
                    </div>
                </div>
            `;
        });
}

function renderizarProductosListones(productos) {
    const container = document.getElementById('productos-listones-container');
    if (!container) {
        console.error('❌ No se encontró el contenedor productos-listones-container');
        return;
    }
    if (productos.length === 0) {
        container.innerHTML = `
            <div class="col-md-12">
                <div class="alert alert-info">
                    <h4>No hay productos disponibles</h4>
                    <p>No se encontraron productos Listones activos en este momento.</p>
                </div>
            </div>
        `;
        return;
    }

    // Orden específico si lo deseas, si no, solo mostrar en el orden recibido
    // const ordenProductos = [ ... ];
    // Si quieres un orden fijo, implementa aquí

    const fallbackPorProducto = {
        'LISTON TRAVERTINO DOBLE': {
            molde: '/static/uploads/Molde - Liston.png',
            mosaico: '/static/uploads/Mosaico - Liston.png'
        },
        'LISTON TRAVERTINO C/ DIENTE': {
            molde: '/static/uploads/Liston 1.png'
        }
    };

    function getFallback(productoNombre, tipo) {
        const key = (productoNombre || '').toUpperCase().trim();
        const cfg = fallbackPorProducto[key] || {};
        return cfg[tipo] || 'img/placeholder.png';
    }

    let html = '';
    productos.forEach((producto, index) => {
        const imagenMolde = producto.imagen_url || 'img/placeholder.png';
        const imagenMosaico = producto.imagen_mosaico_url || '';
        const fallbackMolde = getFallback(producto.nombre, 'molde');
        const fallbackMosaico = getFallback(producto.nombre, 'mosaico');
        let tipoProducto = '';
        let descripcion = producto.descripcion || '';
        switch(producto.nombre) {
            case 'Listones Antideslizantes para Bordes de Piscinas':
                tipoProducto = '';
                descripcion = 'Listones para Piletas. Especialmente diseñados para bordes y zonas de tránsito alrededor de piscinas, ofreciendo una superficie segura, antideslizante y de gran estética. Su diseño alargado aporta elegancia y continuidad visual en el entorno. - Medidas del producto final: 50 x 12,5 x 3,5 cm.';
                break;
            default:
                tipoProducto = '';
        }
        const delay = index * 200;
        html += `
            <div class="col-md-4 producto-animate" data-delay="${delay}">
                <div style="display: flex; flex-direction: row; gap: 24px; justify-content: center; align-items: flex-end;">
                    ${imagenMolde ? `
                    <img src="${imagenMolde}"
                        onerror="this.onerror=null; this.src='${fallbackMolde}';"
                         data-appear-animation="fadeInLeft"
                         data-appear-animation-delay="0"
                         data-plugin-options="{'accY': 10}"
                         alt="${producto.nombre}"
                         class="custom-product-image-pos-1 _relative img-responsive producto-imagen molde-liston"
                         data-delay="${delay + 100}" />
                    ` : ''}
                    ${imagenMosaico ? `
                    <img src="${imagenMosaico}"
                        onerror="this.onerror=null; this.src='${fallbackMosaico}';"
                         data-appear-animation="fadeInLeft"
                         data-appear-animation-delay="200"
                         data-plugin-options="{'accY': 10}"
                         alt="${producto.nombre} - Mosaico"
                         class="custom-product-image-pos-1 _relative img-responsive producto-imagen mosaico-liston"
                         data-delay="${delay + 200}" />
                    ` : ''}
                </div>
            </div>
            <div class="col-md-1"></div>
            <div class="col-md-5 producto-animate" data-delay="${delay}">
                <h4 class="mb-xl mt-xlg producto-titulo" data-delay="${delay + 50}">${producto.nombre}</h4>
                <div class="divider divider-primary divider-small mb-xl producto-titulo" data-delay="${delay + 100}"><hr></div>
                <h4 class="heading-primary">Especificaciones:</h4>
                <p><strong>${tipoProducto}</strong> ${descripcion}</p>
            </div>
            <div class="col-md-12"><hr></div>
        `;
    });
    container.innerHTML = html;
    setTimeout(() => {
        document.querySelectorAll('.producto-animate').forEach(el => el.classList.add('show'));
        document.querySelectorAll('.producto-titulo').forEach(el => el.classList.add('show'));
        document.querySelectorAll('.producto-imagen').forEach(el => el.classList.add('show'));
    }, 100);
    console.log('✅ Productos Listones renderizados con molde y mosaico, tamaño reducido');
}

function activarAnimacionesListones() {
    const productosAnimate = document.querySelectorAll('.producto-animate');
    const titulosAnimate = document.querySelectorAll('.producto-titulo');
    const imagenesAnimate = document.querySelectorAll('.producto-imagen');
    productosAnimate.forEach(elemento => {
        const delay = parseInt(elemento.dataset.delay) || 0;
        setTimeout(() => {
            elemento.classList.add('show');
        }, delay);
    });
    titulosAnimate.forEach(elemento => {
        const delay = parseInt(elemento.dataset.delay) || 0;
        setTimeout(() => {
            elemento.classList.add('show');
        }, delay);
    });
    imagenesAnimate.forEach(elemento => {
        const delay = parseInt(elemento.dataset.delay) || 0;
        setTimeout(() => {
            elemento.classList.add('show');
        }, delay);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 DOM cargado, inicializando carga de productos Listones...');
    cargarProductosListones();

});


window.addEventListener('load', function() {
    const container = document.getElementById('productos-listones-container');
    if (container && container.innerHTML.trim() === '') {
        console.log('🔄 Fallback: cargando productos Listones...');
        cargarProductosListones();
    }
});


