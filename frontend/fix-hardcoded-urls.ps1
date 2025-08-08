# Script para corregir todas las URLs hardcodeadas en el frontend

$rutaFrontend = "c:\Users\lucas\OneDrive\Documentos\GitHub\molpioriginal3\MolpiOriginal2\frontend"

Write-Host "🔧 Corrigiendo URLs hardcodeadas en frontend..." -ForegroundColor Yellow

# Obtener todos los archivos HTML en el frontend
$archivosHTML = Get-ChildItem $rutaFrontend -Recurse -Include "*.html"

$totalArchivos = 0
$totalCorreciones = 0

foreach ($archivo in $archivosHTML) {
    Write-Host "📄 Procesando: $($archivo.Name)" -ForegroundColor Cyan
    
    # Leer contenido
    $contenido = Get-Content $archivo.FullName -Raw -ErrorAction SilentlyContinue
    
    if ($contenido) {
        $contenidoOriginal = $contenido
        
        # Patrones a corregir
        $patrones = @{
            'http://localhost:5000/' = '${window.env.API_URL}/'
            'http://127.0.0.1:5000/' = '${window.env.API_URL}/'
            "'http://localhost:5000/" = "'`${window.env.API_URL}/"
            "'http://127.0.0.1:5000/" = "'`${window.env.API_URL}/"
            '"http://localhost:5000/' = '"`${window.env.API_URL}/'
            '"http://127.0.0.1:5000/' = '"`${window.env.API_URL}/'
        }
        
        $correcciones = 0
        foreach ($patron in $patrones.Keys) {
            $reemplazo = $patrones[$patron]
            $matches = ([regex]::Matches($contenido, [regex]::Escape($patron))).Count
            if ($matches -gt 0) {
                $contenido = $contenido -replace [regex]::Escape($patron), $reemplazo
                $correcciones += $matches
                Write-Host "   ✅ Corregidas $matches ocurrencias de '$patron'" -ForegroundColor Green
            }
        }
        
        if ($correcciones -gt 0) {
            # Hacer backup
            Copy-Item $archivo.FullName "$($archivo.FullName).backup" -Force
            
            # Escribir contenido corregido
            $contenido | Set-Content $archivo.FullName -Encoding UTF8 -Force
            
            $totalArchivos++
            $totalCorreciones += $correcciones
            
            Write-Host "   📦 Backup creado y archivo actualizado" -ForegroundColor Blue
        } else {
            Write-Host "   ℹ️  Sin URLs hardcodeadas encontradas" -ForegroundColor Gray
        }
    }
}

Write-Host ""
Write-Host "📊 RESUMEN:" -ForegroundColor Magenta
Write-Host "   Archivos procesados: $($archivosHTML.Count)" -ForegroundColor White
Write-Host "   Archivos modificados: $totalArchivos" -ForegroundColor Green
Write-Host "   Total de correcciones: $totalCorreciones" -ForegroundColor Green
Write-Host ""
Write-Host "✅ Proceso completado!" -ForegroundColor Green
