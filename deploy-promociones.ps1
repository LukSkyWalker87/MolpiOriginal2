# Script para desplegar cambios de promociones en el servidor
# Ejecutar en PowerShell: .\deploy-promociones.ps1

Write-Host "🟢 INICIANDO DESPLIEGUE DE PROMOCIONES" -ForegroundColor Green
Write-Host ""

# 1. Verificar que estamos en el directorio correcto
Write-Host "1️⃣  Verificando directorio..." -ForegroundColor Cyan
$currentDir = Get-Location
Write-Host "📁 Directorio actual: $currentDir"
if (-not (Test-Path ".git")) {
    Write-Host "❌ ERROR: No es un repositorio git" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Directorio correcto"
Write-Host ""

# 2. Git pull para obtener los cambios
Write-Host "2️⃣  Obteniendo cambios del repositorio..." -ForegroundColor Cyan
git pull
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ ERROR en git pull" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Git pull completado"
Write-Host ""

# 3. Detener contenedores
Write-Host "3️⃣  Deteniendo contenedores Docker..." -ForegroundColor Cyan
docker compose down
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ ERROR al detener contenedores" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Contenedores detenidos"
Write-Host ""

# 4. Reconstruir sin caché
Write-Host "4️⃣  Reconstruyendo Docker sin caché..." -ForegroundColor Cyan
docker compose build --no-cache
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ ERROR en docker compose build" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Docker reconstruido"
Write-Host ""

# 5. Levantar solo el contenedor de la app
Write-Host "5️⃣  Levantando contenedor de la app..." -ForegroundColor Cyan
docker compose up -d
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ ERROR al levantar contenedor" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Contenedor levantado"
Write-Host ""

# 6. Verificar que el archivo está actualizado
Write-Host "6️⃣  Verificando que el archivo se actualizó..." -ForegroundColor Cyan
Write-Host "   Buscando 'molpiFetch' en el contenedor..."
$result = docker exec molpioriginal2-molpi-app-1 grep -c "molpiFetch disponible" /app/www.molpi.com.ar/components/promociones.html 2>$null
if ($result -gt 0) {
    Write-Host "✅ Archivo actualizado correctamente (encontrados $result coincidencias de molpiFetch)"
} else {
    Write-Host "⚠️  ADVERTENCIA: No se encontró 'molpiFetch disponible' en el archivo" -ForegroundColor Yellow
    Write-Host "   Mostrando primeras líneas del archivo:"
    docker exec molpioriginal2-molpi-app-1 head -n 50 /app/www.molpi.com.ar/components/promociones.html
}
Write-Host ""

# 7. Reiniciar nginx
Write-Host "7️⃣  Reiniciando nginx..." -ForegroundColor Cyan
Write-Host "   (Este paso requiere acceso SSH al servidor)" -ForegroundColor Yellow
Write-Host "   Comando manual: sudo systemctl restart nginx"
Write-Host ""

Write-Host "🟢 DESPLIEGUE COMPLETADO" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Próximos pasos:" -ForegroundColor Cyan
Write-Host "  1. Abrí el navegador y ve a https://molpi.com.ar/admin"
Write-Host "  2. Iniciá sesión"
Write-Host "  3. Abrí la consola (F12) y clickeá en 'Eliminar' una promoción"
Write-Host "  4. Deberías ver los nuevos logs con molpiFetch"
Write-Host ""
