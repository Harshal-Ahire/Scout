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

**Scout** is a 4-stage agentic workflow engine designed to reliably ingest, extract, and structure candidate resume data into validated JSON schemas. By combining **EasyOCR** and **Tesseract** for robust text extraction with state-of-the-art LLM reasoning via **LangGraph** and the **Gemini API**, Scout automates fallback handling and retry loops to ensure high accuracy and zero parsing crashes.

---

## Key Capabilities

| Capability | Description |
|---|---|
| **4-Stage Agentic Workflow** | Orchestrated via LangGraph to route documents through parsing, entity extraction, validation, and JSON formatting |
| **Hybrid OCR Text Extraction** | Integrated EasyOCR and Tesseract engines, achieving 92% text extraction accuracy across real-world resume documents |
| **Resilient Fallback Loops** | Automated retry and fallback logic that drops LLM parsing failure rates from 14% to 2% |
| **Structured JSON Schema Output** | Standardizes chaotic resume text into clean, validated JSON payloads ready for ATS integration |
| **Flask REST Backend** | Lightweight API endpoints allowing external services to submit resumes and receive structured candidate profiles |
| **Containerized Deployment** | Fully Dockerized for seamless deployment and consistent environment behavior |

---

## System Architecture

```text
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────────┐     ┌──────────────────┐
│ Resume Document │ ──▶ │ EasyOCR / Tesser-│ ──▶ │ LangGraph 4-Stage   │ ──▶ │ Fallback & Retry │
│ (PDF / Image)   │     │ act OCR Engine   │     │ Processing Workflow │     │ Error Handler    │
└─────────────────┘     └──────────────────┘     └─────────────────────┘     └──────────────────┘
                                                                                      │
                                                                                      ▼
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────────┐     ┌──────────────────┐
│ ATS Integration │ ◀── │ Validated JSON   │ ◀── │ Gemini API Schema   │ ◀── │ Structured State │
│ & HR Dashboard  │     │ Output Schema    │     │ Extraction          │     │ Verification     │
└─────────────────┘     └──────────────────┘     └─────────────────────┘     └──────────────────┘
