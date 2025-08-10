#!/bin/bash

# Deploy script for Google Cloud Run
# Usage: ./deploy.sh [project-id] [region]

PROJECT_ID=${1:-"awesome-destiny-468517-g9"}
REGION=${2:-"asia-northeast1"}
SERVICE_NAME="crypto-alert"

echo "🚀 Deploying Crypto Alert Bot to Google Cloud Run..."
echo "📋 Project: $PROJECT_ID"
echo "🌍 Region: $REGION"
echo "🔧 Service: $SERVICE_NAME"

# Build and deploy using Cloud Build
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --timeout 3600 \
  --concurrency 1 \
  --max-instances 1 \
  --set-env-vars="TZ=Asia/Ho_Chi_Minh"

echo "✅ Deploy completed!"
echo "🔗 Service URL: https://$SERVICE_NAME-$(gcloud config get-value project).$REGION.run.app"
