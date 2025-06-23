#!/bin/bash

# Deploy to Google Cloud Run
# Prerequisites: gcloud CLI configured, Docker installed

set -e

PROJECT_ID=${GOOGLE_CLOUD_PROJECT:-"your-project-id"}
SERVICE_NAME="lazy-logistics-api"
REGION="us-central1"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "Building and deploying to GCP Cloud Run..."

# Build Docker image
echo "Building Docker image..."
docker build -t ${IMAGE_NAME} .

# Push to Google Container Registry
echo "Pushing image to GCR..."
docker push ${IMAGE_NAME}

# Deploy to Cloud Run
echo "Deploying to Cloud Run..."
gcloud run deploy ${SERVICE_NAME} \
    --image ${IMAGE_NAME} \
    --platform managed \
    --region ${REGION} \
    --allow-unauthenticated \
    --set-env-vars="GOOGLE_CLOUD_PROJECT=${PROJECT_ID}" \
    --set-env-vars="CUSTOM_SEARCH_API_KEY=${CUSTOM_SEARCH_API_KEY}" \
    --set-env-vars="CUSTOM_SEARCH_ENGINE_ID=${CUSTOM_SEARCH_ENGINE_ID}" \
    --memory 2Gi \
    --cpu 2 \
    --timeout 300 \
    --concurrency 80

echo "Deployment complete!"
echo "Service URL: $(gcloud run services describe ${SERVICE_NAME} --region=${REGION} --format='value(status.url)')" 