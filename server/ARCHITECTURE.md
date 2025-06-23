# Architecture & Deployment Guide

## High-Level Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Web UI/API    │───▶│  FastAPI Backend │───▶│  Google Search  │
│   (Cloud Run)   │    │   (Cloud Run)    │    │      API        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   Vertex AI      │
                       │  (Gemini 1.5)    │
                       └──────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   Firestore      │
                       │   (Storage)      │
                       └──────────────────┘
```

## GCP Resources Required

### 1. Core Services
- **Vertex AI**: Gemini 1.5 Pro for supplier extraction
- **Custom Search API**: Web document retrieval
- **Firestore**: Data storage and caching
- **Cloud Run**: Application hosting

### 2. Optional Services
- **Cloud Logging**: Application monitoring
- **Cloud Monitoring**: Performance metrics
- **Cloud Trace**: Request tracing
- **Secret Manager**: API key management

## Security Recommendations

### 1. API Key Management
```bash
# Store API keys in Secret Manager
gcloud secrets create custom-search-api-key --data-file=api-key.txt
gcloud secrets create custom-search-engine-id --data-file=engine-id.txt
```

### 2. IAM Permissions
```bash
# Create service account with minimal permissions
gcloud iam service-accounts create lazy-logistics-sa \
    --display-name="Lazy Logistics Service Account"

# Grant necessary permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:lazy-logistics-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:lazy-logistics-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/datastore.user"
```

### 3. Network Security
- Use VPC Connector for private networking
- Enable Cloud Armor for DDoS protection
- Implement rate limiting

## Monitoring & Logging

### 1. Cloud Logging
```python
import logging
from google.cloud import logging

# Configure structured logging
client = logging.Client()
client.setup_logging()

logger = logging.getLogger(__name__)
logger.info("Supplier extraction completed", extra={
    "company_name": company_name,
    "suppliers_found": len(suppliers),
    "processing_time": processing_time
})
```

### 2. Cloud Monitoring
- Create custom metrics for:
  - Extraction success rate
  - Processing time
  - Cache hit rate
  - API usage

### 3. Error Tracking
```python
from google.cloud import error_reporting

error_client = error_reporting.Client()
try:
    # Your code here
    pass
except Exception as e:
    error_client.report_exception()
```

## Scalability Considerations

### 1. Caching Strategy
- Firestore cache with 24-hour TTL
- Redis for session management (optional)
- CDN for static assets

### 2. Rate Limiting
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/extract-suppliers")
@limiter.limit("10/minute")
async def extract_suppliers(request: Request):
    # Your code here
    pass
```

### 3. Async Processing
- Use Cloud Tasks for long-running extractions
- Implement webhook callbacks for results

## Cost Optimization

### 1. Vertex AI
- Use batch predictions for multiple companies
- Implement request batching
- Monitor token usage

### 2. Custom Search API
- Cache results aggressively
- Implement pagination
- Monitor quota usage

### 3. Firestore
- Use appropriate indexes
- Implement data lifecycle policies
- Monitor read/write operations

## Deployment Checklist

- [ ] GCP Project created with billing enabled
- [ ] Required APIs enabled (Vertex AI, Custom Search, Firestore)
- [ ] Service account created with proper permissions
- [ ] API keys stored in Secret Manager
- [ ] Firestore database created
- [ ] Custom Search Engine configured
- [ ] Environment variables configured
- [ ] Docker image built and tested
- [ ] Cloud Run service deployed
- [ ] Monitoring and logging configured
- [ ] Security policies implemented

## Testing

### 1. Unit Tests
```bash
pytest tests/ -v
```

### 2. Integration Tests
```bash
# Test with real GCP services
pytest tests/integration/ -v
```

### 3. Load Testing
```bash
# Use Artillery or similar
artillery run load-test.yml
```

## Troubleshooting

### Common Issues
1. **Authentication errors**: Check service account permissions
2. **API quota exceeded**: Implement rate limiting and caching
3. **Memory issues**: Increase Cloud Run memory allocation
4. **Timeout errors**: Optimize extraction prompts and processing

### Debug Commands
```bash
# Check service logs
gcloud logging read "resource.type=cloud_run_revision" --limit=50

# Monitor API usage
gcloud api-keys list --filter="displayName:custom-search"

# Check Firestore usage
gcloud firestore indexes list
``` 