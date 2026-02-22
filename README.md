# RAGnarok

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)
![CLI](https://img.shields.io/badge/Interface-CLI-orange.svg)

> **RAGnarok**: The last file converter you'll ever need.

RAGnarok is a robust, local-first document ingestion and conversion engine. It takes complex file formats (like messy PDFs) and translates them into semantic, structure-aware Markdown—optimized specifically for Retrieval-Augmented Generation (RAG) pipelines.

## 🌟 Features

- **Standard Parsing Layer**: Out-of-the-box support for `pdfplumber` to extract both text and table structures.
- **Heuristic Validation**: Automatically evaluates layout integrity, tracking text-to-symbol ratios and column drift to assign confidence scores (OCR, Layout, Overall).
- **Selective VLM Repair**: When the heuristic engine catches a corrupted page, RAGnarok interfaces with a local Vision Language Model (VLM) via Ollama (e.g., LLaVA) to selectively repair garbled text and broken tables.
- **Semantic RAG Chunking**: Context-aware chunking that keeps tables together, prepends semantic metadata (`<!-- RAG METADATA -->`), and enforces logical token sizes.
- **Diagnostics & Reporting**: Built-in sidecar JSON reporting detailing page-by-page confidence for deterministic tracing.

---

## 🚀 Installation

Ensure you have Python 3.10+ and [uv](https://github.com/astral-sh/uv) installed.

```bash
# Clone the repository
git clone https://github.com/pronzzz/RAGnarok.git
cd RAGnarok

# Setup the environment with uv
uv sync
```

---

## 💻 Usage

Run the CLI tool directly using your project's script endpoint:

```bash
ragnarok path/to/document.pdf 
```

### Advanced Flags

- `-o, --output`: Specify the output path for the Markdown file.
- `-v, --verbose`: Enable verbose logging to see heuristic validation steps.
- `--report`: Generate a structural JSON confidence report sidecar detailing corruption indices.
- `--dry-run`: Parse and validate the document without writing output to disk.
- `--debug`: Enable debug mode with detailed execution traces.

**Example**:

```bash
ragnarok document.pdf --output result.md --report --verbose
```

---

## 🏗️ Architecture Walkthrough

1. **CLI Foundation**: Powered by `argparse`, orchestrating target paths and flags.
2. **Intermediate Representation**: Uses `DocumentIIR` (Internal Intermediate Representation) heavily utilizing Python `dataclasses` (Pages, Blocks, Headings, Tables).
3. **Parse & Validate**: Passes through `pdfplumber` to `heuristics.py`.
4. **Heal**: `repair.py` catches Low-Confidence Pages (< 0.7 Score) and delegates to local Ollama.
5. **Chunk**: `chunking.py` slices the healed representation into RAG-safe blocks while injecting metadata.

---

## 🤝 Contributing

We welcome contributions! See our [CONTRIBUTING.md](CONTRIBUTING.md) guide for more details and read our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before submitting a pull request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
