<div align="center">

# Scout — AI Recruitment Workflow Engine

**Semantic candidate evaluation at scale, powered by LLM agents.**

Scout replaces keyword-matching resume screeners with a context-aware AI pipeline that reasons about skill depth, role alignment, and candidate fit — cutting manual screening effort by **65%**.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Backend-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![Gemini](https://img.shields.io/badge/Gemini_2.0_Flash-LLM-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[**Live Demo**](#) · [**Report Bug**](#) · [**Request Feature**](#)

</div>

---

## Table of Contents

- [Why Scout](#why-scout)
- [Key Capabilities](#key-capabilities)
- [System Architecture](#system-architecture)
- [Pipeline Breakdown](#pipeline-breakdown)
- [Engineering Highlights](#engineering-highlights)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Performance Impact](#performance-impact)
- [Roadmap](#roadmap)
- [Design Philosophy](#design-philosophy)
- [License](#license)

---

## Why Scout

Traditional applicant tracking systems filter resumes by keyword frequency — a method that rewards resume-stuffing over genuine competence and misses strong candidates who phrase things differently than a job description.

Scout takes a different approach. It's an **agentic evaluation pipeline** built on Google Gemini 2.0 Flash that reads resumes the way a thoughtful recruiter would: understanding context, weighing skill depth against role requirements, and producing structured, defensible evaluations — at a scale no human team could match.

> Instead of *"does this resume contain the word 'Python'?"*, Scout asks *"does this candidate's experience demonstrate the depth this role actually requires?"*

---

## Key Capabilities

| Capability | Description |
|---|---|
| 🧠 **Semantic Candidate Evaluation** | LLM-based assessment of resumes against role context, not keyword frequency |
| 📦 **High-Throughput Processing** | Bulk ingestion via ZIP archives or individual PDF / DOCX / TXT uploads |
| 🧹 **Document Normalization Pipeline** | Converts heterogeneous formats into clean, structured text for reliable AI processing |
| 🤖 **Agentic Workflow Execution** | Multi-step pipeline where the LLM plans, calls tools (parsers, CSV generators), and evaluates outcomes |
| 🔁 **Resilient Inference Layer** | Retry logic with exponential backoff to handle rate limits and transient API failures |
| 📊 **Structured Output Generation** | Converts unstructured AI reasoning into clean CSV output for HR systems and analytics |

---

## System Architecture

```
┌────────┐     ┌────────────┐     ┌───────────────┐     ┌───────────────┐     ┌────────────────┐
│ Upload │ ──▶ │ Extraction │ ──▶ │ Normalization │ ──▶ │ LLM Inference │ ──▶ │ Structured Output│
└────────┘     └────────────┘     └───────────────┘     └───────────────┘     └────────────────┘
   ZIP/PDF/         Unpack &          Clean, unify         Semantic scoring,      CSV export /
   DOCX/TXT         parse files       text format           entity extraction     HR integration
```

The system is deliberately split into independent stages so that each layer — ingestion, transformation, inference, and output — can be scaled, tested, and swapped out without touching the rest of the pipeline.

---

## Pipeline Breakdown

**1. Ingestion**
Accepts bulk uploads (ZIP archives) and individual files. Extracts and validates documents before they enter the pipeline.

**2. Normalization**
Parses PDF and DOCX documents into consistent, clean text — stripping formatting noise while preserving semantic structure (sections, bullet points, dates).

**3. Inference**
The LLM performs:
- Semantic evaluation of experience against role requirements
- Skill and entity extraction
- Relevance scoring with justification

**4. Output Layer**
Persists results and generates structured CSV output ready for downstream HR tooling.

---

## Engineering Highlights

- **AI embedded in production workflows** — Gemini calls are orchestrated as part of a structured pipeline with defined inputs/outputs, not fired off as isolated, unstructured API calls.
- **Pipeline-oriented architecture** — clean separation of concerns across ingestion, transformation, inference, and output layers.
- **Production robustness** — retry mechanisms, structured logging, and observability built in from the start to handle noisy real-world data and API rate limits.
- **Scalable processing** — designed to hold up under concurrent, high-volume batch workloads without performance degradation.

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python, Flask |
| **AI Engine** | Google Gemini 2.0 Flash |
| **Document Parsing** | PyMuPDF (`fitz`), python-docx |
| **Frontend** | React, JavaScript, Tailwind CSS |
| **Deployment** | Render |

---

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- A Google Gemini API key

### Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/scout.git
cd scout

# Backend setup
cd backend
pip install -r requirements.txt
cp .env.example .env        # add your GEMINI_API_KEY
python app.py

# Frontend setup
cd ../frontend
npm install
npm run dev
```

The app will be available at `http://localhost:5173` (frontend) with the API running on `http://localhost:5000`.

---

## Project Structure

```
scout/
├── backend/
│   ├── app.py                # Flask entry point
│   ├── pipeline/
│   │   ├── ingestion.py       # Upload & extraction
│   │   ├── normalization.py   # Document cleaning
│   │   ├── inference.py       # Gemini-powered evaluation
│   │   └── output.py          # CSV generation
│   └── requirements.txt
├── frontend/
│   ├── src/
│   └── package.json
└── README.md
```

> Update this tree to match your actual repo layout.

---

## Performance Impact

- **~65% reduction** in manual screening effort
- Improved candidate-role matching through semantic (vs. keyword) analysis
- Stable processing under concurrent, high-volume workloads

---

## Roadmap

- [ ] Embedding-based candidate ranking (vector similarity search)
- [ ] Human-in-the-loop feedback and correction system
- [ ] Native ATS / HRIS integrations
- [ ] Benchmark suite for evaluating model scoring quality

---

## Design Philosophy

Scout is built as a **practical AI system**, prioritizing:

1. **Reliability over experimentation** — every LLM call is wrapped in retries, logging, and validation.
2. **Workflow integration over isolated intelligence** — the model is one stage in a pipeline, not a black box.
3. **Scalable handling of real-world data** — built to survive messy resumes, inconsistent formatting, and API limits.

---

## License

Distributed under the MIT License. See `LICENSE` for details.

<div align="center">

If you found this project interesting, consider giving it a ⭐

</div>
