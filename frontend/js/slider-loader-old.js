document.addEventListener('DOMContentLoaded', () => {
    const sliderContainer = document.querySelector('.tp-revslider-slides');
    
    fetch('/json/slider_content.json')
      .then(response => response.json())
      .then(slides => {
        if (!sliderContainer) return;
  
        sliderContainer.innerHTML = ''; // Limpiar sliders actuales
  
        slides.forEach((slide, index) => {
          if (!slide.activo) return;
  
          const li = document.createElement('li');
          li.setAttribute('data-transition', 'fade');
  
          li.innerHTML = `
            <img src="${slide.fondo}" alt="" class="rev-slidebg" data-bgposition="center center" data-bgfit="cover" data-bgrepeat="no-repeat">
            
            <div class="tp-caption main-label" data-x="50" data-y="150" data-start="1000">
              ${slide.titulo}
            </div>
            
            <div class="tp-caption bottom-label" data-x="50" data-y="220" data-start="1400">
              ${slide.descripcion}
            </div>
  
            ${slide.imagen ? `<div class="tp-caption" data-x="right" data-y="100" data-start="1800">
              <img src="${slide.imagen}" alt="">
            </div>` : ''}
          `;
  
          sliderContainer.appendChild(li);
        });
      })
      .catch(err => console.error('Error cargando slider:', err));
  });
  