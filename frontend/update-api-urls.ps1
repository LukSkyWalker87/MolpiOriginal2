# Script para actualizar todas las URLs de API en el frontend

# Lista de archivos a procesar
$archivos = @(
    "admin.html",
    "insumos_nuevo.html", 
    "piscinas_nuevo.html",
    "placas_antihumedad_dinamico.html",
    "podotactiles.html",
    "revestimientos_nuevo.html",
    "components\productos.html",
    "components\testimonios.html",
    "components\promociones.html"
)

$rutaFrontend = "c:\Users\lucas\OneDrive\Documentos\GitHub\molpioriginal3\MolpiOriginal2\frontend"

foreach ($archivo in $archivos) {
    $rutaCompleta = Join-Path $rutaFrontend $archivo
    
    if (Test-Path $rutaCompleta) {
        Write-Host "Procesando: $archivo" -ForegroundColor Green
        
        # Leer contenido
        $contenido = Get-Content $rutaCompleta -Raw -Encoding UTF8
        
        # Reemplazar todas las URLs de API
        $contenido = $contenido -replace "fetch\('\/productos", "fetch(`${window.env.API_URL}/productos"
        $contenido = $contenido -replace "fetch\('\/testimonios", "fetch(`${window.env.API_URL}/testimonios"
        $contenido = $contenido -replace "fetch\('\/promociones", "fetch(`${window.env.API_URL}/promociones"
        $contenido = $contenido -replace "fetch\('\/login", "fetch(`${window.env.API_URL}/login"
        $contenido = $contenido -replace "fetch\('\/categorias", "fetch(`${window.env.API_URL}/categorias"
        $contenido = $contenido -replace "fetch\('\/subcategorias", "fetch(`${window.env.API_URL}/subcategorias"
        
        # Reemplazar con comillas dobles también
        $contenido = $contenido -replace 'fetch\("\/productos', 'fetch(`${window.env.API_URL}/productos'
        $contenido = $contenido -replace 'fetch\("\/testimonios', 'fetch(`${window.env.API_URL}/testimonios'
        $contenido = $contenido -replace 'fetch\("\/promociones', 'fetch(`${window.env.API_URL}/promociones'
        $contenido = $contenido -replace 'fetch\("\/login', 'fetch(`${window.env.API_URL}/login'
        $contenido = $contenido -replace 'fetch\("\/categorias', 'fetch(`${window.env.API_URL}/categorias'
        $contenido = $contenido -replace 'fetch\("\/subcategorias', 'fetch(`${window.env.API_URL}/subcategorias'
        
        # Escribir contenido actualizado
        Set-Content $rutaCompleta $contenido -Encoding UTF8
        
        Write-Host "Actualizado: $archivo" -ForegroundColor Yellow
    } else {
        Write-Host "No encontrado: $archivo" -ForegroundColor Red
    }
}

Write-Host "¡Actualización completada!" -ForegroundColor Cyan
