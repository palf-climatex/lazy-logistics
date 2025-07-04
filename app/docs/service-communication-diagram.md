# Service Communication Diagram

## Overview
This document describes the service communication architecture of the Lazy Logistics UI application, which is a React-based frontend that communicates with a Python backend API for supplier extraction.

## Architecture Components

```
┌─────────────────────────────────────────────────────────────────┐
│                        Lazy Logistics UI                        │
│                         (Frontend)                              │
├─────────────────────────────────────────────────────────────────┤
│  React 18.2.0 + Vite + Tailwind CSS + SWR                      │
│  Port: 5173/5174 (Development)                                  │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ HTTP/JSON
                                │ POST /extract-suppliers
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Backend API Service                          │
│                         (Python)                                │
├─────────────────────────────────────────────────────────────────┤
│  FastAPI/Flask/Django (Port: 8000)                              │
│  Supplier Extraction Engine                                     │
└─────────────────────────────────────────────────────────────────┘
```

## Detailed Communication Flow

### 1. API Connection Test
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Clicks   │───▶│  Frontend       │───▶│  Backend API    │
│  Test Button    │    │  testDirectAPI()│    │  POST /extract- │
│                 │    │                 │    │  suppliers      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │  Success/Fail   │◀───│  Response       │
                       │  Indicator      │    │  JSON           │
                       └─────────────────┘    └─────────────────┘
```

### 2. Supplier Extraction Flow
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Enters   │───▶│  Form Submit    │───▶│  SWR Hook       │
│  Company Name   │    │  (Enter Key)    │    │  useSWR         │
│   + Presses     │    │                 │    │                 │
│     Enter       │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │  State Update   │───▶│  API Request    │
                       │  shouldFetch    │    │  POST with      │
                       │  = true         │    │  company_name   │
                       └─────────────────┘    └─────────────────┘
                                                        │
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │  Backend API    │
                                               │  Processing     │
                                               │  (30s timeout)  │
                                               └─────────────────┘
                                                        │
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │  Response       │
                                               │  JSON Data      │
                                               └─────────────────┘
                                                        │
                                                        │
                                                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │  UI Update      │◀───│  SWR Cache      │
                       │  Results        │    │  & State        │
                       │  Display        │    │  Update         │
                       └─────────────────┘    └─────────────────┘
```

## API Endpoints

### POST /extract-suppliers
**URL:** `http://localhost:8000/extract-suppliers`  
**Method:** POST  
**Content-Type:** application/json  
**Accept:** application/json  

#### Request Body
```json
{
  "company_name": "string",
  "limit": 10
}
```

#### Response Format
```json
{
  "suppliers": [
    {
      "name": "string",
      "confidence": 0.95,
      "context": "string",
      "source_url": "string"
    }
  ],
  "total_suppliers": 5,
  "processing_time": 2.34
}
```

## Error Handling

### Timeout Handling
- **Frontend:** 30-second timeout with AbortController
- **Backend:** Expected to handle long-running extraction tasks
- **User Feedback:** Loading spinners and error messages

### Error States
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Network Error  │───▶│  Error Display  │───▶│  User Retry     │
│  Timeout        │    │  Component      │    │  or Reset       │
│  HTTP 4xx/5xx   │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## State Management

### Frontend State
```javascript
{
  companyName: string,        // User input
  shouldFetch: boolean,       // SWR trigger
  searchTerm: string,         // Actual search term
  data: object,              // API response
  error: Error,              // Error state
  isLoading: boolean,        // Loading state
  apiTestSuccess: boolean    // Connection test result
}
```

### SWR Configuration
```javascript
{
  revalidateOnFocus: false,
  revalidateOnReconnect: false,
  shouldRetryOnError: false
}
```

## Security Considerations

### CORS
- Frontend runs on `localhost:5173/5174`
- Backend expected on `localhost:8000`
- CORS headers required for cross-origin requests

### Input Validation
- Frontend validates non-empty company names
- Backend should validate and sanitize inputs
- Rate limiting recommended

## Performance Optimizations

### Caching Strategy
- SWR provides automatic caching
- Cache key: `extract-suppliers-${searchTerm}`
- Prevents duplicate requests for same company

### Request Optimization
- 30-second timeout prevents hanging requests
- AbortController allows request cancellation
- Limit parameter reduces response size

## Development Workflow

### Local Development
1. **Frontend:** `npm run dev` (Port 5173/5174)
2. **Backend:** Expected on `localhost:8000`
3. **API Testing:** Built-in test button for connection verification

### Build Process
1. **Development:** Vite dev server with HMR
2. **Production:** `npm run build` → Static files in `/dist`
3. **Preview:** `npm run preview` for production testing

## Dependencies

### Frontend Dependencies
- **React 18.2.0:** UI framework
- **SWR 2.1.5:** Data fetching and caching
- **Vite:** Build tool and dev server
- **Tailwind CSS:** Styling framework

### Development Dependencies
- **PostCSS:** CSS processing
- **Autoprefixer:** CSS vendor prefixes
- **Testing Libraries:** Jest, React Testing Library

## Monitoring and Debugging

### Console Logging
- API request/response logging
- State change tracking
- Error logging with stack traces

### Network Monitoring
- Browser DevTools Network tab
- Request/response inspection
- Performance timing analysis 