// Este script maneja el envío del formulario de productos y muestra un mensaje de error si el producto ya existe

document.addEventListener('DOMContentLoaded', function () {
  const formProducto = document.getElementById('formProducto');
  if (!formProducto) return;

  // Crear o reutilizar un contenedor para mensajes de error
  let errorDiv = document.getElementById('productoErrorMsg');
  if (!errorDiv) {
    errorDiv = document.createElement('div');
    errorDiv.id = 'productoErrorMsg';
    errorDiv.className = 'alert alert-danger mt-2';
    errorDiv.style.display = 'none';
    formProducto.prepend(errorDiv);
  }

  formProducto.addEventListener('submit', async function (e) {
    e.preventDefault();
    errorDiv.style.display = 'none';
    errorDiv.textContent = '';

    const formData = new FormData(formProducto);
    const data = {};
    formData.forEach((value, key) => {
      data[key] = value;
    });

    try {
      const response = await fetch('/producto', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });
      if (response.status === 409) {
        const res = await response.json();
        errorDiv.textContent = res.error || 'El producto ya existe.';
        errorDiv.style.display = 'block';
        return;
      }
      if (!response.ok) {
        errorDiv.textContent = 'Error al guardar el producto.';
        errorDiv.style.display = 'block';
        return;
      }
      // Si todo sale bien, cerrar modal y refrescar productos
      $('#modalProducto').modal('hide');
      // Aquí deberías recargar la tabla de productos, por ejemplo:
      if (typeof cargarProductos === 'function') cargarProductos();
    } catch (err) {
      errorDiv.textContent = 'Error de red o del servidor.';
      errorDiv.style.display = 'block';
    }
  });
});
