<img width="1475" height="704" alt="Results" src="https://github.com/user-attachments/assets/0045ecdd-7b9b-43fb-9942-5c32df8fd72a" />
<img width="1911" height="912" alt="uploading" src="https://github.com/user-attachments/assets/000c4397-19bb-48bd-82cc-42cec8601dee" />
<img width="1918" height="906" alt="Home" src="https://github.com/user-attachments/assets/91748f7b-49b7-4e4c-90b7-6597497bee4d" />
<div align="center">


<div align="center">

# Scout — AI-Powered Resume Screening Engine

**An automated agentic workflow platform that parses, validates, and extracts structured JSON schemas from unstructured resume documents using LangGraph, OCR, and Gemini API.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agentic_Workflows-1C3C3C)](https://www.langchain.com/)
[![Flask](https://img.shields.io/badge/Flask-Backend-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![OCR](https://img.shields.io/badge/OCR-EasyOCR_%7C_Tesseract-FF6F00)](https://github.com/JaidedAI/EasyOCR)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[**GitHub**](https://github.com/Harshal-Ahire/Scout) · [**Report Bug**](https://github.com/Harshal-Ahire/Scout/issues) · [**Request Feature**](https://github.com/Harshal-Ahire/Scout/issues)

</div>

---

## Table of Contents

- [Overview](#overview)
- [Key Capabilities](#key-capabilities)
- [System Architecture](#system-architecture)
- [Agentic Parsing Pipeline](#agentic-parsing-pipeline)
- [Engineering Highlights](#engineering-highlights)
- [Performance & Benchmark Impact](#performance--benchmark-impact)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Example Usage](#example-usage)
- [Project Structure](#project-structure)
- [Roadmap](#roadmap)
- [License](#license)

---

## Overview

Traditional resume parsing tools break down when faced with complex layouts, non-standard formatting, or scanned PDF documents, leading to missing skill profiles and extraction errors.

**Scout** is a 4-stage agentic workflow engine designed to reliably ingest, extract, and structure candidate resume data into validated JSON schemas. By combining **EasyOCR** and **Tesseract** for robust text extraction with LLM reasoning via **LangGraph** and the **Gemini API**, Scout automates fallback handling and retry loops to improve extraction reliability and reduce parsing failures.

---

## Key Capabilities

| Capability | Description |
|---|---|
| **4-Stage Agentic Workflow** | Orchestrated via LangGraph to route documents through parsing, entity extraction, validation, and JSON formatting |
| **Hybrid OCR Text Extraction** | Integrates EasyOCR and Tesseract engines, achieving 92% text extraction accuracy across real-world resume documents |
| **Resilient Fallback Loops** | Automated retry and fallback logic that reduces LLM parsing failure rates from 14% to 2% |
| **Structured JSON Schema Output** | Standardizes unstructured resume text into clean, validated JSON payloads ready for ATS integration |
| **Flask REST Backend** | Lightweight API endpoints allowing external services to submit resumes and receive structured candidate profiles |
| **Containerized Deployment** | Dockerized deployment for consistent environments and simplified setup |

---

## System Architecture

```text
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────────┐     ┌──────────────────┐
│ Resume Document │ ──▶ │ EasyOCR /        │ ──▶ │ LangGraph 4-Stage   │ ──▶ │ Fallback & Retry │
│ (PDF / Image)   │     │ Tesseract OCR    │     │ Processing Workflow │     │ Error Handler    │
└─────────────────┘     └──────────────────┘     └─────────────────────┘     └──────────────────┘
                                                                                      │
                                                                                      ▼
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────────┐     ┌──────────────────┐
│ ATS Integration │ ◀── │ Validated JSON   │ ◀── │ Gemini API Schema   │ ◀── │ Structured State │
│ & HR Dashboard  │     │ Output Schema    │     │ Extraction          │     │ Verification     │
└─────────────────┘     └──────────────────┘     └─────────────────────┘     └──────────────────┘
```

---

## Agentic Parsing Pipeline

1. **Document Ingestion & OCR** — Accepts PDF documents and image-based resumes, routing them through EasyOCR and Tesseract to extract textual information. The reported text extraction accuracy is 92% across test documents.

2. **State Initialization & Routing** — Passes extracted text into a LangGraph state machine designed to manage multi-step processing phases.

3. **Gemini Entity Extraction** — Uses the Gemini API to identify candidate attributes, including skills, work experience, education, and projects, and map them to structured fields.

4. **Validation & Retry Loop** — Verifies extracted output against JSON schemas and triggers fallback or retry logic when formatting or extraction errors occur. The reported parsing failure rate drops from 14% to 2%.

---

## Engineering Highlights

- **Fault-Tolerant State Machines:** Uses LangGraph to handle messy, unstructured inputs and coordinate processing across multiple stages.

- **Robust OCR Fallback Strategy:** Combines multiple OCR engines to improve text extraction from low-quality scans and image-based resumes.

- **Strict Schema Enforcement:** Validates extracted data to improve downstream compatibility and triggers corrective processing when output is malformed.

- **Modular Architecture:** Separates workflow orchestration, OCR extraction, state management, and schema validation for easier testing and maintenance.

---

## Performance & Benchmark Impact

| Metric | Result | Description |
|---|---|---|
| **Text Extraction Accuracy** | 92% | Evaluated across 50 real-world resume documents with diverse layouts |
| **Parsing Failure Rate** | 14% → 2% | Reduction attributed to automated LLM fallback handling and retry loops |
| **Workflow Stages** | 4-stage engine | Orchestrated using LangGraph, from document ingestion to validated JSON output |

*Note: Benchmark figures are reported project metrics. Reproducible evaluation results depend on the test dataset, evaluation criteria, and execution environment.*

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language & Core | Python 3.10+ |
| Workflow Orchestration | LangGraph, LangChain |
| AI / LLM Engine | Gemini API |
| Backend Framework | Flask |
| OCR & Vision | EasyOCR, Tesseract OCR |
| Data Validation | Pydantic / Custom JSON Schema Validators |
| Testing & Quality | pytest |
| Deployment | Docker, Docker Compose |

---

## Getting Started

### Prerequisites

- Python 3.10+
- Tesseract OCR installed locally or available through the Docker environment
- Docker
- Docker Compose
- Gemini API key

### Quick Start with Docker

```bash
# Clone the repository
git clone https://github.com/Harshal-Ahire/Scout.git
cd Scout

# Set up environment variables
cp .env.example .env

# Add your GEMINI_API_KEY to the .env file

# Build and start the service
docker compose up --build -d
```

The Flask service will be available at:

- **API Base URL:** http://localhost:5000

### Run Local Tests

```bash
# Run the test suite
pytest tests/ -v
```

---

## Example Usage

### Submit a Resume for Parsing

The following example submits a PDF resume to the parsing endpoint.

```bash
curl -X POST "http://localhost:5000/api/v1/parse" \
  -H "Content-Type: multipart/form-data" \
  -F "resume=@/path/to/resume.pdf"
```

Replace `/path/to/resume.pdf` with the path to your resume file.

### Expected JSON Response

```json
{
  "status": "success",
  "candidate": {
    "name": "Example Candidate",
    "email": "candidate@example.com",
    "skills": [
      "Python",
      "LangGraph",
      "FastAPI",
      "Docker"
    ],
    "experience": [
      {
        "role": "AI Engineer Intern",
        "company": "Example Company",
        "duration": "Jan 2026 - Jun 2026"
      }
    ]
  }
}
```

*The response above is illustrative. Actual fields and values depend on the resume content and the API implementation.*

---

## Project Structure

```text
Scout/
├── app/
│   ├── main.py                 # Flask application entry point
│   ├── agents/
│   │   ├── workflow.py         # LangGraph 4-stage agentic workflow
│   │   └── state.py            # State definitions and schemas
│   ├── ocr/
│   │   └── extractor.py        # EasyOCR and Tesseract integration
│   └── utils/
│       └── validators.py       # JSON schema validation and retry logic
├── tests/
│   ├── test_ocr.py             # OCR extraction accuracy tests
│   └── test_workflow.py        # LangGraph routing and retry tests
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Roadmap

- [x] Implement the 4-stage LangGraph agentic workflow.
- [x] Integrate EasyOCR and Tesseract for text extraction.
- [x] Implement automated fallback and retry loops.
- [ ] Expand parser support for multi-page executive CV formats.
- [ ] Build a lightweight web dashboard for HR candidate review.
- [ ] Expand evaluation coverage across complex resume layouts and document formats.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**Developed by Harshal Ahire** · If you found this repository useful, give it a ⭐!
