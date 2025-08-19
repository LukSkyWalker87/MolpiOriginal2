// Este archivo se creó para forzar una actualización de caché
// Versión: 7 de Agosto de 2025 - 13:00 - Campo Estado con formato sutil

// Asegurarse que el campo Estado funcione correctamente
document.addEventListener('DOMContentLoaded', function() {
  console.log('⚠️ Versión actualizada - Campo Estado con formato sutil');

  // Verificar el campo Estado al abrir el modal
  const modalProducto = document.getElementById('modalProducto');
  if (modalProducto) {
    modalProducto.addEventListener('shown.bs.modal', function() {
      const productoEstado = document.getElementById('productoEstado');
      if (productoEstado) {
        console.log('✅ Campo Estado cargado correctamente con formato sutil');
        
        // Agregar listener para cambios
        productoEstado.addEventListener('change', function() {
          console.log('🔄 Estado cambiado a:', this.value === '1' ? 'Activo' : 'Inactivo');
        });
        
      } else {
        console.error('❌ Campo Estado no encontrado');
      }
    });
  }
});

// Función para verificar si el campo Estado está funcionando correctamente
window.verificarCampoEstado = function() {
  const productoEstado = document.getElementById('productoEstado');
  
  if (!productoEstado) {
    console.error('❌ Campo Estado no encontrado en el DOM');
    return false;
  }
  
  console.log('✅ Campo Estado encontrado con valor:', productoEstado.value);
  console.log('✅ Campo Estado con formato sutil');
  return true;
}
