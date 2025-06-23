# Lazy Logistics UI

A React frontend application for extracting supplier information using Tailwind CSS and SWR.

## Features

- Clean, modern UI with Tailwind CSS
- Form to input company name
- POSTs to `http://localhost:8000/extract-suppliers`
- Displays extracted supplier data in a list
- Error handling and loading states
- Responsive design

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

The app will run on `http://localhost:3000`

## Usage

1. Enter a company name in the input field
2. Click "Extract Suppliers" to send a POST request
3. View the extracted supplier data in the list below
4. Use "Reset" to clear the form and results

## API Endpoint

The app expects a backend API running on `http://localhost:8000` with the endpoint:
- `POST /extract-suppliers`
- Request body: `{ "company_name": "string" }`
- Response: Array of supplier objects or strings

## Technologies

- React 18
- Tailwind CSS
- SWR for data fetching
- Create React App 