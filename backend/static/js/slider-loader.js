console.log('🛠️ slider-loader.js cargado correctamente');

document.addEventListener('DOMContentLoaded', () => {
  console.log('📦 DOM listo, iniciando carga de slider...');

  fetch('json/slider_content.json')
    .then(res => res.json())
    .then(data => {
      console.log('📂 JSON recibido:', data);

      const container = document.querySelector('#revolutionSlider');
      if (!container) {
        console.error('❌ No se encontró #revolutionSlider');
        return;
      }

      let ul = container.querySelector('ul');
      if (!ul) {
        ul = document.createElement('ul');
        container.appendChild(ul);
        console.log('✅ <ul> creado dinámicamente');
      }

      ul.innerHTML = ''; // Limpiar previos

      data.forEach(slide => {
        const li = document.createElement('li');
        li.setAttribute('data-transition', 'fade');

        const fondo = document.createElement('img');
        fondo.src = slide.fondo;
        fondo.className = 'rev-slidebg';
        fondo.setAttribute('data-bgposition', 'center center');
        fondo.setAttribute('data-bgfit', 'cover');
        fondo.setAttribute('data-bgrepeat', 'no-repeat');
        li.appendChild(fondo);

        slide.elementos.forEach(el => {
          const div = document.createElement('div');
          div.classList.add('tp-caption');
          
          if (el.class) {
            el.class
              .split(' ')
              .filter(cl => cl.trim() && /^[a-zA-Z0-9_-]+$/.test(cl))
              .forEach(cl => div.classList.add(cl));
          }
          

          if (el.data_x) div.setAttribute('data-x', el.data_x);
          if (el.data_y) div.setAttribute('data-y', el.data_y);
          if (el.data_start) div.setAttribute('data-start', el.data_start);
          if (el.data_transform) div.setAttribute('data-transform_in', el.data_transform);
          if (el.data_mask) div.setAttribute('data-mask_in', el.data_mask);

          if (el.tipo === 'img') {
            const img = document.createElement('img');
            img.src = el.src;
            img.alt = '';
            div.appendChild(img);
          }

          if (el.tipo === 'text') {
            div.innerText = el.texto;
          }

          li.appendChild(div);
        });

        ul.appendChild(li);
      });

      // Inicializar Revolution Slider
      setTimeout(() => {
        const liCount = document.querySelectorAll('#revolutionSlider ul li').length;
        if (liCount > 0 && window.jQuery && jQuery().revolution) {
          console.log(`🚀 Inicializando Revolution Slider con ${liCount} slides`);
          jQuery('#revolutionSlider').show().revolution({
            delay: 9000,
            gridwidth: 1170,
            gridheight: 550,
            disableProgressBar: 'on'
          });
        } else {
          console.warn('⚠️ Aún no hay slides cargados o Revolution no está disponible');
        }
      }, 600);
    })
    .catch(err => console.error('❌ Error en carga de slider:', err));
});
