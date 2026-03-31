import os, glob

files = [
    'backend/templates/revestimientos.html',
    'backend/templates/revestimientos_dinamico.html',
    'frontend/revestimientos.html',
    'frontend/revestimientos_dinamico.html',
    'www.molpi.com.ar/revestimientos.html',
    'www.molpi.com.ar/revestimientos_dinamico.html'
]

css_desktop = """
		.custom-product-image-container .mosaico-pinotea-ajuste {
			top: 90px !important;
			left: 60px !important;
		}

		@media (max-width: 767px) {"""

css_mobile = """
			.custom-product-image-container .mosaico-pinotea-ajuste {
				top: 70px !important;
				left: 45px !important;
			}
		}"""

for path in files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Inject CSS desktop
    if "		@media (max-width: 767px) {" in content:
        content = content.replace("		@media (max-width: 767px) {", css_desktop, 1)
    elif "			@media (max-width: 767px) {" in content:
        content = content.replace("			@media (max-width: 767px) {", css_desktop.replace('\t', '\t\t'), 1)
        
    # Inject CSS mobile
    if "		}\n	</style>" in content:
        content = content.replace("		}\n	</style>", css_mobile + "\n	</style>", 1)
    elif "			}\n		</style>" in content:
        content = content.replace("			}\n		</style>", css_mobile.replace('\t', '\t\t') + "\n		</style>", 1)

    # Inject esPinotea
    find_line = "const tieneMosaico = producto.imagen_mosaico_url && producto.imagen_mosaico_url.trim() !== '' && !producto.imagen_mosaico_url.includes('.html');"
    # Or in non-dinamico:
    find_line2 = "const tieneMosaico = producto.imagen_mosaico_url &&\n\t\t\t\t\tproducto.imagen_mosaico_url.trim() !== '' &&\n\t\t\t\t\t!producto.imagen_mosaico_url.includes('.html'); // Excluir URLs incorrectas con .html"
    
    replace_line = find_line + "\n\t\t\t\t\t\t\tconst esPinotea = (producto.nombre || '').toLowerCase().includes('pinotea');"
    replace_line2 = find_line2 + "\n\t\t\t\tconst esPinotea = (producto.nombre || '').toLowerCase().includes('pinotea');"

    if find_line in content:
        content = content.replace(find_line, replace_line)
    elif find_line2 in content:
        content = content.replace(find_line2, replace_line2)

    # Inject class to mosaic
    content = content.replace("class=\"custom-product-image-pos-5 _absolute img-responsive\"", "class=\"custom-product-image-pos-5 _absolute img-responsive ${esPinotea ? 'mosaico-pinotea-ajuste' : ''}\"")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
