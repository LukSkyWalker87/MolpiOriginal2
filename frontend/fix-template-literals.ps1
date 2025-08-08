# Script para corregir automáticamente template literals en archivos HTML

$rutaArchivo = "c:\Users\lucas\OneDrive\Documentos\GitHub\molpioriginal3\MolpiOriginal2\frontend\admin.html"

Write-Host "Corrigiendo template literals en admin.html..." -ForegroundColor Yellow

# Leer el contenido del archivo
$contenido = Get-Content $rutaArchivo -Raw -ErrorAction SilentlyContinue

if ($contenido) {
    # Corregir patrones comunes de errores
    $contenidoCorregido = $contenido
    
    # Patrón 1: fetch(${window.env.API_URL}/endpoint')
    $contenidoCorregido = $contenidoCorregido -replace 'fetch\(\$\{window\.env\.API_URL\}\/([^\']+)\'\)', 'fetch(`${window.env.API_URL}/$1`)'
    
    # Patrón 2: fetch('${window.env.API_URL}/endpoint')
    $contenidoCorregido = $contenidoCorregido -replace "fetch\('\$\{window\.env\.API_URL\}\/([^']+)'\)", 'fetch(`${window.env.API_URL}/$1`)'
    
    # Verificar si hubo cambios
    if ($contenido -ne $contenidoCorregido) {
        # Hacer backup
        Copy-Item $rutaArchivo "$rutaArchivo.backup" -Force
        
        # Escribir el contenido corregido
        $contenidoCorregido | Set-Content $rutaArchivo -Encoding UTF8 -Force
        
        Write-Host "✅ Archivo corregido exitosamente" -ForegroundColor Green
        Write-Host "📦 Backup creado: admin.html.backup" -ForegroundColor Blue
    } else {
        Write-Host "ℹ️  No se encontraron errores para corregir" -ForegroundColor Cyan
    }
} else {
    Write-Host "❌ No se pudo leer el archivo" -ForegroundColor Red
}

Write-Host "✅ Proceso completado" -ForegroundColor Green
