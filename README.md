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
- [Roadmap](#roadmap)
- [License](#license)

---

## Overview

Traditional resume parsing tools struggle with complex layouts, non-standard formatting, and scanned PDF documents, often resulting in missing candidate information and extraction errors.

**Scout** is a 4-stage agentic workflow engine designed to ingest, extract, and structure resume data into validated JSON schemas. By combining **EasyOCR** and **Tesseract** for text extraction with **LangGraph** and the **Gemini API** for LLM-powered reasoning, Scout automates fallback handling and retry loops to improve extraction reliability and reduce parsing failures.

---

## Key Capabilities

| Capability | Description |
|---|---|
| **4-Stage Agentic Workflow** | Orchestrates resume processing through parsing, entity extraction, validation, and JSON formatting using LangGraph |
| **Hybrid OCR Text Extraction** | Integrates EasyOCR and Tesseract, achieving 92% text extraction accuracy across tested resume documents |
| **Resilient Fallback Loops** | Automated retry and fallback logic reduces reported LLM parsing failure rates from 14% to 2% |
| **Structured JSON Schema Output** | Converts unstructured resume text into validated JSON payloads suitable for applicant tracking system (ATS) integration |
| **Flask REST Backend** | Provides API endpoints for submitting resumes and retrieving structured candidate profiles |
| **Containerized Deployment** | Uses Docker for consistent environments and simplified deployment |

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

1. **Document Ingestion & OCR** — Accepts PDF documents and image-based resumes, using EasyOCR and Tesseract to extract textual information.

2. **State Initialization & Routing** — Passes extracted text into a LangGraph state machine that manages multi-stage processing and coordinates workflow transitions.

3. **Gemini Entity Extraction** — Uses the Gemini API to identify candidate attributes, including skills, work experience, education, and projects, and maps them to structured fields.

4. **Validation & Retry Loop** — Validates extracted output against JSON schemas and triggers fallback or retry logic when formatting or extraction errors occur.

---

## Engineering Highlights

- **Fault-Tolerant State Machines:** LangGraph coordinates processing stages and manages workflow transitions for unstructured resume inputs.

- **Robust OCR Fallback Strategy:** Combines EasyOCR and Tesseract to improve text extraction from scanned documents and low-quality images.

- **Strict Schema Enforcement:** Validates extracted data and triggers corrective processing when the generated output does not meet the expected schema.

- **Modular Processing Pipeline:** Separates workflow orchestration, OCR extraction, state management, and validation to simplify testing and maintenance.

---

## Performance & Benchmark Impact

| Metric | Result | Description |
|---|---|---|
| **Text Extraction Accuracy** | 92% | Reported accuracy across 50 resume documents with diverse layouts |
| **Parsing Failure Rate** | 14% → 2% | Reported reduction through automated fallback handling and retry loops |
| **Workflow Stages** | 4 stages | LangGraph orchestration from document ingestion to validated JSON output |

*Note: Performance figures are reported project metrics and should be supported by reproducible benchmark results.*

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language & Core | Python 3.10+ |
| Workflow Orchestration | LangGraph, LangChain |
| AI / LLM Engine | Gemini API |
| Backend Framework | Flask |
| OCR & Vision | EasyOCR, Tesseract OCR |
| Data Validation | Pydantic, Custom JSON Schema Validators |
| Testing & Quality | pytest |
| Deployment | Docker, Docker Compose |

---

## Getting Started

### Prerequisites

- Python 3.10+
- Tesseract OCR installed locally or configured in the Docker environment
- Docker
- Docker Compose
- Gemini API key

### Quick Start with Docker

```bash
# Clone the repository
git clone https://github.com/Harshal-Ahire/Scout.git
cd Scout

# Configure environment variables
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

*The JSON above is an illustrative example. Actual fields and values depend on the resume content and the API implementation.*

---

## Roadmap

- [x] Implement the 4-stage LangGraph agentic workflow.
- [x] Integrate EasyOCR and Tesseract for text extraction.
- [x] Implement automated fallback and retry loops.
- [ ] Expand parser support for multi-page executive CV formats.
- [ ] Build a lightweight HR dashboard for candidate review.
- [ ] Expand evaluation coverage across complex resume layouts and document formats.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

**Developed by Harshal Ahire** · If you found this repository useful, give it a ⭐!
