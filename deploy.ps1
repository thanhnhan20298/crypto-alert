# PowerShell Deploy Script for Google Cloud Run
# Usage: .\deploy.ps1 -ProjectId "your-project-id" -Region "asia-southeast1"

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectId,
    
    [Parameter(Mandatory=$false)]
    [string]$Region = "asia-southeast1",
    
    [Parameter(Mandatory=$false)]
    [string]$ServiceName = "crypto-alert"
)

Write-Host "🚀 Deploying Crypto Alert Bot to Google Cloud Run..." -ForegroundColor Green
Write-Host "📋 Project: $ProjectId" -ForegroundColor Cyan
Write-Host "🌍 Region: $Region" -ForegroundColor Cyan
Write-Host "🔧 Service: $ServiceName" -ForegroundColor Cyan

try {
    # Set project
    Write-Host "Setting project..." -ForegroundColor Yellow
    gcloud config set project $ProjectId
    
    # Build image using Cloud Build
    Write-Host "Building Docker image..." -ForegroundColor Yellow
    gcloud builds submit --tag "gcr.io/$ProjectId/$ServiceName"
    
    # Deploy to Cloud Run
    Write-Host "Deploying to Cloud Run..." -ForegroundColor Yellow
    gcloud run deploy $ServiceName `
        --image "gcr.io/$ProjectId/$ServiceName" `
        --platform managed `
        --region $Region `
        --allow-unauthenticated `
        --memory 512Mi `
        --cpu 1 `
        --timeout 3600 `
        --concurrency 1 `
        --max-instances 1 `
        --set-env-vars="TZ=Asia/Ho_Chi_Minh"
    
    Write-Host "✅ Deploy completed successfully!" -ForegroundColor Green
    
    # Get service URL
    $serviceUrl = gcloud run services describe $ServiceName --region=$Region --format="value(status.url)"
    Write-Host "🔗 Service URL: $serviceUrl" -ForegroundColor Cyan
    
} catch {
    Write-Host "❌ Deploy failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
