# CODE_REVIEW.md

## RAGnarok Code Review & Analysis

Here is a comprehensive code review of the RAGnarok project, separated into key categories.

### 1. Code Quality

* **Hardcoded Defaults**: In `src/ragnarok/repair.py:12`, the `ollama_url` defaults to `http://localhost:11434/api/generate`. While convenient for local tools, hardcoded API endpoints can be considered a code smell. Consider reading from environment variables (e.g., `os.getenv("OLLAMA_URL", "...")`) or standard config files.
* **Missing Docstrings**: Some dataclasses in `src/ragnarok/models.py` (e.g., `Paragraph`, `Heading`, `TableRow`) lack descriptive docstrings. While self-explanatory, consistency in documentation is a best practice.
* **Lazy Imports**: In `cli.py:25` and `cli.py:43`, imports like `from ragnarok.orchestrator import Orchestrator` are placed inside the function. Given this is a CLI, lazy importing can improve startup time, so it is an acceptable pattern, but it should be documented.

### 2. Bug Detection

* **Directory Handling (Logic Error)**:
  * **File**: `src/ragnarok/cli.py` (Lines 10, 31-36) & `src/ragnarok/orchestrator.py` (Lines 20-30).
  * **Issue**: The CLI argument help states `help="Path to input file or directory"`. However, if a directory is passed to `args.input`, `os.path.splitext(args.input)` will return `("dirname", "")`. The `orchestrator.py` will then fail with `ValueError("Unsupported file format: ")` because `ext` is empty.
  * **Suggestion**: Implement directory traversal in `cli.py` (e.g., `os.walk` or `pathlib.Path.rglob`) to iterate over all files and call the orchestrator for each valid file, or update the CLI to state it only accepts files.
* **Fragile URL Parsing (Logic Error)**:
  * **File**: `src/ragnarok/repair.py` (Line 21).
  * **Issue**: `requests.get(self.ollama_url.replace("/api/generate", ""), timeout=1)`. This relies on a strict string replacement. If `ollama_url` lacks this exact path, it will request the generation endpoint with a GET request, which Ollama might reject or hang on.
  * **Suggestion**: Use `urllib.parse.urlparse` to extract the scheme and netloc to build the base URL reliably.

### 3. Security Analysis

* **SSRF Vector**:
  * **File**: `src/ragnarok/repair.py` (Line 52).
  * **Issue**: `requests.post(self.ollama_url, ...)` makes requested based on a potentially user-configurable URL. If the CLI is run on a server or as part of an automated pipeline with untrusted config, this can lead to Server-Side Request Forgery (SSRF).
  * **Suggestion**: Validate the host of the URL against a whitelist of allowed domains or strictly bound it to localhost/internal IPs if intended purely for local VLM instances.
* **Path Traversal/Validation**: Output paths constructed in `cli.py` lack explicit sanitization. Being a CLI tool, this is lower risk, but path traversal issues could arise if `args.output` is generated programmatically.

### 4. Performance

* **String Concatenation in Loops**:
  * **File**: `src/ragnarok/chunking.py` (Lines 39-42).
  * **Issue**: Using `+=` for string concatenation inside a loop (e.g., `block_md += "| " + ...`) is technically \(O(N^2)\) due to string immutability in Python.
  * **Suggestion**: Append segments to a local list and use `"".join()` at the end of the block processing for optimal performance.
* **Synchronous Processing**:
  * **File**: `src/ragnarok/parsers/pdf.py`.
  * **Issue**: Page extraction happens synchronously. For 100+ page PDFs, `pdfplumber` can be slow.
  * **Suggestion**: Consider using a `ProcessPoolExecutor` from `concurrent.futures` to extract pages in parallel where structural order can be reconstituted afterwards.

### 5. Best Practices

* **Error Handling**: In `src/ragnarok/cli.py:52`, catching generic `Exception` is an anti-pattern. Catching specific exceptions (`FileNotFoundError`, `ValueError`) provides clearer error boundaries and allows unexpected bugs to surface correctly.
* **Typing**: You are effectively using Python type hints (`from typing import ...`). Continuing to enforce this with tools like `mypy` is highly recommended.
* **Test Coverage**: There are currently 6 files in `tests/` based on standard directory listings, but it's important to verify edge cases (e.g., corrupted PDFs, VLM timeouts, empty documents) are strictly covered.
