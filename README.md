## Pytest Playwright Test Automation Demo

### Introduction
This project has been created to showcase the basic structure for a test automation project based on pytest and playwright.
It provides demo tests for web UI and API.

### SUT
Tests are provided for https://automationexercise.com/ - a practice website for Automation Engineers.

---

## Environment Setup Guide

### Prerequisites

- **Python 3.12+** — required ([download](https://www.python.org/downloads/))
- **Git** — to clone the repository
- **Poetry** *(optional)* — for dependency management via lockfile

Verify your Python version:
```bash
python --version
```

---

### 1. Clone the Repository

```bash
git clone <repository-url>
cd pytest-playwright-ui-api
```

---

### 2. Install Dependencies

Choose either **pip** or **Poetry**:

#### Option A — pip

```bash
# Create and activate a virtual environment
python -m venv .venv

# Activate (Linux / macOS / WSL)
source .venv/bin/activate

# Activate (Windows — Command Prompt)
.venv\Scripts\activate.bat

# Activate (Windows — PowerShell)
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

#### Option B — Poetry (recommended)

Poetry manages a reproducible virtual environment using the lockfile. The project is configured to create the `.venv` inside the project directory.

**Install Poetry (if not already installed):**

```bash
# Linux / macOS / WSL
curl -sSL https://install.python-poetry.org | python3 -

# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

After installation, restart your terminal and verify:
```bash
poetry --version
```

> If `poetry` is not found after installation, add the Poetry binary directory to your `PATH`.
> The installer prints the exact path to add — typically `~/.local/bin` on Linux/macOS or `%APPDATA%\Python\Scripts` on Windows.

**Install project dependencies:**

```bash
poetry install
```

This creates a `.venv` inside the project and installs all dependencies from `pyproject.toml`.

---

### 3. Install Playwright Browsers

Playwright requires browser binaries to be downloaded separately after the Python packages are installed.

```bash
# pip
python -m playwright install --with-deps

# Poetry
poetry run playwright install --with-deps
```

`--with-deps` also installs OS-level system dependencies (required on Linux/CI).

---

### 4. Configuration

#### `settings.toml`

Environment settings live in `settings.toml`. Tests default to the `qa` environment:

```toml
[qa]
base_url = "https://automationexercise.com"
```

Add settings for other environments (`dev`, `uat`, `prod`) in the same file as needed.

#### `.secrets.toml` (git-ignored)

For secrets (credentials, tokens, etc.), create a `.secrets.toml` file in the project root — it is listed in `.gitignore` and will never be committed:

```toml
[qa]
username = "your-username"
password = "your-password"
```

#### Environment Variable Overrides

Any setting can be overridden at runtime with a `DYNACONF_` prefixed environment variable:

```bash
# Override base URL
export DYNACONF_BASE_URL="https://staging.example.com"

# Override a secret
export DYNACONF_PASSWORD="secret123"
```

---

### 5. Verify the Setup

Run the smoke tests to confirm everything is working:

```bash
# pip
pytest -m smoke

# Poetry
poetry run pytest -m smoke
```

---

## Running Tests

```bash
# All tests (headed browser, screenshots on failure by default)
pytest tests

# Single file
pytest tests/test_api.py

# Single test by name
pytest tests/test_api.py::test_get_product_list

# By marker
pytest -m smoke
pytest -m quality_gate

# Parallel execution (skip tests marked `single`)
pytest -n auto -m "not single"

```

### Test Markers

| Marker | Description |
|--------|-------------|
| `smoke` | Smoke tests |
| `single` | Must not run in parallel |
| `mobile` | Mobile-only tests |
| `quality_gate` | Quality gate tests |

---

## Project Structure

```
pytest-playwright-ui-api/
├── config.py               # Dynaconf settings loader
├── settings.toml           # Per-environment configuration
├── .secrets.toml           # Secrets (git-ignored, create manually)
├── requirements.txt        # pip dependencies
├── pyproject.toml          # Project metadata + pytest config
├── page_objects/
│   ├── page_creator.py     # PageCreator facade (injected via `ui` fixture)
│   └── *.py                # Individual page object classes
└── tests/
    ├── conftest.py         # Fixtures: browser, context, ui, api, faker
    ├── test_api.py
    └── test_ui.py
```

---

## Linting

```bash
ruff check .
```

---

## CI/CD

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `ruff_check.yml` | Every push | Lint check |
| `run_all_tests.yml` | Manual (`workflow_dispatch`) | Full test suite |
