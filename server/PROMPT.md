
You are my AI pair programmer.

I want to build a tool that takes a company name as input and returns a list of its suppliers. The solution should combine retrieval + GenAI extraction using GCP resources.

Please help me create an initial architecture, code scaffold, and cloud resource plan. The system should have the following components:

1️⃣ Input:

    User submits a company name (e.g., "Tesco") via an API endpoint or simple web UI.

2️⃣ Retrieval layer:

    Use external APIs (Google Programmable Search API or Bing Search API) to retrieve web documents mentioning the company and possible suppliers.

    Integrate Google Custom Search API via GCP.

3️⃣ Extraction layer:

    Use Vertex AI with Gemini 1.5 Pro or PaLM 2 models to perform entity extraction on the retrieved documents.

    Prompt the LLM to extract any supplier names mentioned.

    Output should be structured JSON (list of supplier names with optional confidence score and source reference).

4️⃣ Aggregation layer:

    Deduplicate supplier names (basic fuzzy matching).

    Merge mentions across multiple documents.

    Optional: store raw documents and extractions in BigQuery or Firestore for future audits.

5️⃣ Output:

    Return a cleaned supplier list to the user via the API or frontend.

6️⃣ Cloud resources:

    GCP Project setup

    Vertex AI GenAI models

    Google Custom Search API

    Cloud Functions (or Cloud Run for backend)

    Firestore / BigQuery for data storage

    (Optional: deploy Streamlit frontend via Cloud Run)

7️⃣ Coding stack preferences:

    Python 3.12

    FastAPI for API backend

    Use google-cloud-* official Python SDKs for accessing GCP resources.

    Use openai, google.generativeai or vertexai libraries for LLM interaction.

Task:
Please begin by generating:

    Full GCP architecture diagram (high-level)

    Initial Python code scaffold (directory structure and main files)

    Example code for:

        calling Google Programmable Search API

        calling Vertex AI model with a prompt to extract suppliers

        API endpoint using FastAPI to submit a company name and return supplier list

Assume I have the necessary API keys and GCP billing/project setup already.

Also include:

    Initial example prompt for the LLM extraction.

    Recommendations for security and scalability.

    Suggestions for monitoring/logging using GCP tools.

I will iterate from your output.
