document.addEventListener('DOMContentLoaded', () => {
  const sidebarLinks = document.querySelectorAll('.sidebar a');
  const contentArea = document.querySelector('.main-content');

  let slidesData = [];

  // Navegación dinámica entre secciones
  sidebarLinks.forEach(link => {
    link.addEventListener('click', async function (e) {
      e.preventDefault();

      // Activar estilo
      sidebarLinks.forEach(l => l.classList.remove('active'));
      this.classList.add('active');

      // Cargar contenido dinámico
      const section = this.getAttribute('data-section');
      try {
        const res = await fetch(`/admin/component/${section}`);
        const html = await res.text();
        contentArea.innerHTML = html;

        // Inicializar lógica si es el slider
        if (section === 'slider') {
          initSliderEditor();
        }
      } catch (err) {
        contentArea.innerHTML = '<p class="text-danger">Error al cargar el componente</p>';
        console.error(err);
      }
    });
  });

// Cargar el slider editable al cargar la página
  function cargarSliderEditable() {
    fetch('/data/slider_content.json')
      .then(res => res.json())
      .then(slides => {
        const container = document.getElementById('slider-container');
        container.innerHTML = '';
  
        slides.forEach((slide, index) => {
          const card = document.createElement('div');
          card.className = 'card mb-3';
          card.innerHTML = `
            <div class="card-header">
              <strong>Slide ${index + 1}</strong>
            </div>
            <div class="card-body">
              <form class="slide-form" data-index="${index}">
                <div class="form-group">
                  <label>Título</label>
                  <input type="text" class="form-control" name="title" value="${slide.title}">
                </div>
                <div class="form-group">
                  <label>Descripción</label>
                  <textarea class="form-control" name="description" rows="2">${slide.description}</textarea>
                </div>
                <div class="form-group">
                  <label>Imagen</label>
                  <input type="text" class="form-control" name="image_url" value="${slide.image_url}">
                </div>
                <div class="form-group">
                  <label>Posición del texto</label>
                  <select class="form-control" name="position">
                    <option value="left" ${slide.position === 'left' ? 'selected' : ''}>Izquierda</option>
                    <option value="center" ${slide.position === 'center' ? 'selected' : ''}>Centro</option>
                    <option value="right" ${slide.position === 'right' ? 'selected' : ''}>Derecha</option>
                  </select>
                </div>
                <div class="form-check mb-2">
                  <input class="form-check-input" type="checkbox" name="active" ${slide.active ? 'checked' : ''}>
                  <label class="form-check-label">Activo</label>
                </div>
                <button type="button" class="btn btn-primary btn-sm guardar-slide">Guardar</button>
              </form>
            </div>
          `;
          container.appendChild(card);
        });
  
        // Guardar cambios en slide
        document.querySelectorAll('.guardar-slide').forEach(btn => {
          btn.addEventListener('click', function () {
            const form = this.closest('.slide-form');
            const index = form.dataset.index;
            const data = {
              title: form.title.value,
              description: form.description.value,
              image_url: form.image_url.value,
              position: form.position.value,
              active: form.active.checked
            };
  
            guardarSlide(index, data);
          });
        });
      });
  }
  
  function guardarSlide(index, data) {
    fetch(`/admin/guardar_slide/${index}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    }).then(res => res.json())
      .then(resp => alert(resp.message))
      .catch(err => alert("Error al guardar el slide"));
  }
  
  
  // Cargar sección por defecto
  const defaultLink = document.querySelector('.sidebar a[data-section="dashboard"]');
  if (defaultLink) defaultLink.click();

  // Lógica del editor de slides
  function initSliderEditor() {
    const contenedor = document.getElementById('slider-editor');
    const botonGuardar = document.getElementById('guardar-slides');

    if (!contenedor || !botonGuardar) return;

    fetch('/datos_slider')
      .then(res => res.json())
      .then(data => {
        slidesData = Array.isArray(data) ? data : [data];
        renderSlides();
      })
      .catch(err => {
        contenedor.innerHTML = '<p class="text-danger">Error al cargar el slider</p>';
        console.error('Error al cargar JSON:', err);
      });

    function renderSlides() {
      contenedor.innerHTML = '';
      slidesData.forEach((slide, index) => {
        const div = document.createElement('div');
        div.className = 'card p-3 mb-3';
        div.innerHTML = `
          <h5>Slide ${index + 1}</h5>
          <div class="form-group">
            <label>Título</label>
            <input type="text" class="form-control" value="${slide.titulo || ''}" onchange="actualizarCampo(${index}, 'titulo', this.value)">
          </div>
          <div class="form-group">
            <label>Descripción</label>
            <input type="text" class="form-control" value="${slide.descripcion || ''}" onchange="actualizarCampo(${index}, 'descripcion', this.value)">
          </div>
          <div class="form-group">
            <label>Imagen URL</label>
            <input type="text" class="form-control" value="${slide.imagen || ''}" onchange="actualizarCampo(${index}, 'imagen', this.value)">
          </div>
        `;
        contenedor.appendChild(div);
      });
    }

    // Hacer accesible desde el DOM global
    window.actualizarCampo = (index, campo, valor) => {
      slidesData[index][campo] = valor;
    };

    botonGuardar.addEventListener('click', () => {
      fetch('/admin/slider', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(slidesData)
      })
        .then(res => res.json())
        .then(data => {
          alert(data.message || 'Guardado con éxito');
        })
        .catch(err => {
          console.error('Error al guardar:', err);
          alert('Ocurrió un error al guardar');
        });
    });
  }
});

