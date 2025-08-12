# Variables (ajusta si cambiaste algo)
$PROJECT_ID = "molpi-26525"
$REGION = "us-central1"
$REPO = "molpi-docker"
$IMAGE = "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO/molpi-app:latest"

# 1. Autenticación Docker con Artifact Registry (solo la primera vez)
gcloud auth configure-docker "$REGION-docker.pkg.dev"

# 2. Build y push de la imagen
docker build -t $IMAGE .
docker push $IMAGE

# 3. Desplegar en Cloud Run
gcloud run deploy molpi-app `
  --image $IMAGE `
  --region $REGION `
  --allow-unauthenticated `
  --port 8080 `
  --cpu 1 --memory 512Mi --min-instances 0

# 4. Obtener la URL pública
gcloud run services describe molpi-app --region $REGION --format="value(status.url)"