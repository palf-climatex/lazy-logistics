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
6. **Filtering Layer**: Supplier ignore list for excluding unwanted results
7. **Output Layer**: Structured JSON response with supplier list

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
SUPPLIER_IGNORE_LIST_FILE=supplier_ignore_list.txt  # Optional: path to ignore list file
```

### Installation
```bash
pip install -r requirements.txt
```

### Running Locally
```bash
. .venv/bin/activate
uv sync
uv run uvicorn app.main:app --reload
```

## API Endpoints

### Core Endpoints
- `POST /extract-suppliers`: Submit company name, get supplier list
- `GET /health`: Health check endpoint
- `GET /history/{company_name}`: Get extraction history for a company
- `GET /statistics`: Get basic statistics about extractions

### Ignore List Management
- `GET /ignore-list`: Get the current supplier ignore list
- `POST /ignore-list/add`: Add a supplier to the ignore list
- `DELETE /ignore-list/remove`: Remove a supplier from the ignore list
- `POST /ignore-list/reload`: Reload the ignore list from file

### Ignore List Usage
The ignore list allows you to exclude specific suppliers from extraction results. This is useful for:
- Filtering out false positives
- Excluding internal subsidiaries
- Removing generic or placeholder supplier names

The ignore list is stored in a text file (default: `suppliers/supplier_ignore_list.txt`) with one supplier name per line. Lines starting with `#` are treated as comments.

Example ignore list:
```
# Common false positives
Unknown Supplier
Generic Supplier
Test Supplier
Example Corp
```

## Project Structure
```
lazy-logistics/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── config.py            # Configuration management
│   ├── services/
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
├── suppliers/               # Supplier data and analysis
│   ├── supplier_ignore_list.txt
│   ├── suppliers_*.json
│   └── supplier_analysis.json
├── requirements.txt
├── Dockerfile
└── README.md
```
