# Lazy Logistics - Supplier Extraction Tool

A GCP-powered tool that extracts supplier information for companies using retrieval + GenAI extraction.

## Architecture

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

## Components

1. **Input Layer**: FastAPI backend accepting company names
2. **Retrieval Layer**: Google Custom Search API for web document retrieval
3. **Extraction Layer**: Vertex AI Gemini 1.5 for supplier entity extraction
4. **Aggregation Layer**: Deduplication and merging of supplier mentions
5. **Storage Layer**: Firestore for caching and audit trails
6. **Output Layer**: Structured JSON response with supplier list

## Setup

### Prerequisites
- GCP Project with billing enabled
- Vertex AI API enabled
- Custom Search API enabled
- Firestore database created

### Environment Variables
```bash
GOOGLE_CLOUD_PROJECT=your-project-id
CUSTOM_SEARCH_API_KEY=your-search-api-key
CUSTOM_SEARCH_ENGINE_ID=your-search-engine-id
```

### Installation
```bash
pip install -r requirements.txt
```

### Running Locally
```bash
uvicorn app.main:app --reload
```

## API Endpoints

- `POST /extract-suppliers`: Submit company name, get supplier list
- `GET /health`: Health check endpoint

## Project Structure
```
lazy-logistics/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   │   ├── __init__.py
│   │   ├── search.py        # Google Search API
│   │   ├── extraction.py    # Vertex AI extraction
│   │   └── storage.py       # Firestore operations
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py       # Pydantic models
│   └── utils/
│       ├── __init__.py
│       └── deduplication.py # Fuzzy matching
├── requirements.txt
├── Dockerfile
└── README.md
``` 