# Contributing to RAGnarok

First off, thanks for taking the time to contribute! RAGnarok aims to build a world-class standard for local, private document ingestion.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an Issue outlining:

- The OS and environment.
- The command run.
- Expected vs. Actual behavior.

### Suggesting Enhancements

We love new feature ideas! If there's a file parser you want to see (like `.docx` or `.html`), feel free to propose it in the Issues tab before starting work.

### Pull Requests

1. Fork the repo and create your branch from `main`.
2. Ensure you have activated the environment using `uv`.
3. If you've added code that should be tested, add tests in the `tests/` directory.
4. Issue a Pull Request detailing the specific changes made and why.

## Development Setup

```bash
git clone https://github.com/pronzzz/RAGnarok.git
cd RAGnarok
uv sync
```

Please adhere to standard PEP-8 style guidelines.
