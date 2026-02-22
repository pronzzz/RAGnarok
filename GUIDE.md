# RAGnarok Technical Guide

## System Overview

RAGnarok is designed to ingest complex file formats—specifically messy PDFs—and convert them into a clean, RAG-optimized markdown format.

It operates on a phased intelligence approach:

1. **Extraction**: Best-effort layout parsing.
2. **Validation**: Heuristic analysis.
3. **Healing**: VLM fallback for corrupted pages.
4. **Chunking**: Semantic context tracking.

## Core Modules

### 1. The Parser Layer (`parsers/pdf.py`)

Relies on `pdfplumber`. Extracts text and explicitly bounds tables, cleaning up empty cells, and returning a tree of `Page` -> `Table`/`Paragraph` blocks forming the `DocumentIIR`.

### 2. The Heuristic Layer (`heuristics.py`)

Iterates over the `DocumentIIR` evaluating text quality.

- **OCR Checks**: Ensures high symbol-to-alphanumeric ratios.
- **Layout Checks**: Scans for aggressive column drifting (very short lines consistently wrapping).
Assigns an `overall` confidence score ranging from 0.0 to 1.0. A score `< 0.7` flags the page as corrupted.

### 3. The Repair Layer (`repair.py`)

If local Ollama is running (defaults to `:11434`), RAGnarok passes corrupted pages to a Vision/Language model. The model is prompted to rebuild the layout of the text into correct structural Markdown.

*Note: In future production iterations, passing the physical image slice of the PDF page to LLaVA will yield standard SOTA results.*

### 4. Semantic Chunking (`chunking.py`)

Converts the internal AST into Markdown. Crucially, it tracks bounding tokens. It will never slice a table block in half. Once the token count (heuristically 1.3 tokens/word) exceeds `max_tokens` (default 1000), it injects an HTML comment header:

```html
<!-- RAG METADATA: {"page": 2, "hierarchy": "Introduction > Target Audience"} -->
```

## Local VLM Environment Setup

To fully utilize RAGnarok's capabilities, ensure you have Ollama installed locally.

1. Install [Ollama](https://ollama.com).
2. Pull the default repair model:

   ```bash
   ollama pull llava
   ```

3. Ensure the server is running when you execute `ragnarok`. If the server is offline, RAGnarok gracefully degrades and skips the repair attempt.
