// Ejecuta este código en la consola del navegador cuando tengas abierto el modal de editar Green Rombos

console.log('=== DIAGNÓSTICO CAMPO ESTADO ===');

// Verificar si el campo Estado existe
const productoEstado = document.getElementById('productoEstado');
console.log('Campo Estado encontrado:', !!productoEstado);
console.log('Elemento Estado:', productoEstado);

if (productoEstado) {
    console.log('Valor actual:', productoEstado.value);
    console.log('Opciones disponibles:', Array.from(productoEstado.options).map(o => ({value: o.value, text: o.text})));
    console.log('Visible:', productoEstado.offsetWidth > 0 && productoEstado.offsetHeight > 0);
    console.log('Estilos:', productoEstado.style.cssText);
    
    // Destacar el campo
    productoEstado.style.border = '5px solid red';
    productoEstado.style.backgroundColor = 'yellow';
    
    console.log('✅ Campo Estado destacado con borde rojo y fondo amarillo');
} else {
    console.log('❌ Campo Estado NO encontrado');
}

// Verificar todos los elementos del formulario
const form = document.getElementById('formProducto');
if (form) {
    const elementos = form.querySelectorAll('input, select, textarea');
    console.log('Elementos del formulario:', elementos.length);
    elementos.forEach((el, i) => {
        if (el.id) console.log(`${i}: ${el.tagName} - ID: ${el.id} - Name: ${el.name}`);
    });
}
