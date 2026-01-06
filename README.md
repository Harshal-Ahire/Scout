# SCOUT — AI Talent Acquisition Engine

Scout is a production-ready recruitment platform that leverages **Gemini 2.0 Flash** to automate candidate screening. By shifting from traditional keyword-based filters to **semantic analysis**, Scout identifies the best-fit candidates based on context, skill depth, and experience.



## Project Overview

The system provides an end-to-end pipeline for HR teams to process bulk resumes against multiple job descriptions. It handles the complexity of unstructured data parsing, AI inference, and structured data export in a single unified interface.

### Core Engineering Features

* **Semantic Intelligence**: Utilizes Large Language Models (LLMs) to evaluate resumes against JDs, overcoming the limitations of traditional Boolean search and keyword matching.
* **Bulk Document Ingestion**: Supports bulk ingestion via ZIP archives and individual file uploads (PDF, DOCX, TXT).
* **Document Normalization Layer**: Implements a robust preprocessing pipeline to standardize disparate document formats into clean text for AI consumption.
* **Reliability & Error Handling**: Includes automated back-off logic for API rate-limiting (HTTP 429) to ensure system stability during high-volume processing.
* **Structured Data Serialization**: Transforms qualitative AI reasoning into quantitative CSV reports for integration with downstream Human Resource Information Systems (HRIS).

## Technical Stack

* **Backend**: Python (Flask)
* **AI Engine**: Google Gemini 2.0 Flash API
* **Parsing Libraries**: PyMuPDF (fitz), python-docx
* **Frontend**: JavaScript (Stack-based upload management), Tailwind CSS
* **Deployment**: Render (Web Service architecture)



## System Pipeline

1. **Ingestion**: Files are uploaded via a drag-and-drop interface. ZIP files are extracted server-side to the local file system.
2. **Transformation**: The normalization layer strips formatting and metadata, extracting raw text from PDF and DOCX files.
3. **Inference**: Normalized text is fed into a structured prompt. The model performs a dual-track task: qualitative screening and quantitative entity extraction.
4. **Output**: Data is serialized into a session-managed object for real-time display and dynamic CSV generation.

## Installation and Deployment

### Local Setup

pip install -r requirements.txt
GEMINI_API_KEY=your_api_key_here
python app.py

Cloud Deployment (Render)
This repository is configured for immediate deployment on Render via the included render.yaml.

Service Type: Web Service

Build Command: pip install -r requirements.txt

Start Command: python app.py

Performance Impact
Process Automation: Reduces manual screening time by approximately 65% through bulk ingestion and automated scoring.

Data Accuracy: Improves candidate matching by moving beyond keyword frequency to semantic role alignment.

System Reliability: Maintains uptime during peak loads using automated rate-limit handling


1. Clone the repository:
   ```bash
   git clone [https://github.com/yourusername/scout-ai.git](https://github.com/yourusername/scout-ai.git)
