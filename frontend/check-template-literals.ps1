# Script para verificar y corregir template literals en archivos HTML

$rutaFrontend = "c:\Users\lucas\OneDrive\Documentos\GitHub\molpioriginal3\MolpiOriginal2\frontend"

# Buscar archivos con errores de template literals
Get-ChildItem $rutaFrontend -Recurse -Include "*.html" | ForEach-Object {
    $archivo = $_.FullName
    $contenido = Get-Content $archivo -Raw -ErrorAction SilentlyContinue
    
    if ($contenido) {
        # Buscar patrones incorrectos
        $patronesIncorrectos = @(
            'fetch\([$]{window\.env\.API_URL}[^`]',
            'fetch\([^`][^$]*[$]{window\.env\.API_URL}'
        )
        
        foreach ($patron in $patronesIncorrectos) {
            if ($contenido -match $patron) {
                Write-Host "⚠️  Posible error en: $($_.Name)" -ForegroundColor Yellow
                
                # Mostrar líneas problemáticas
                $lineas = $contenido -split "`n"
                for ($i = 0; $i -lt $lineas.Length; $i++) {
                    if ($lineas[$i] -match $patron) {
                        Write-Host "   Línea $($i+1): $($lineas[$i].Trim())" -ForegroundColor Red
                    }
                }
                Write-Host ""
            }
        }
    }
}

Write-Host "✅ Verificación completada" -ForegroundColor Green
