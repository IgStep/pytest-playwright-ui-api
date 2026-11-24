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
# All tests (headless, screenshots on failure)
pytest tests

# API tests only: no browser needed, ~20 s in parallel
pytest tests/api -n auto

# UI tests only
pytest tests/ui

# Single file / single test
pytest tests/api/test_search_product.py
pytest tests/api/test_verify_login.py::test_verify_login_with_valid_credentials

# By marker
pytest -m smoke
pytest -m "api and smoke"
pytest -m contract

# Parallel execution (skip tests marked `single`)
pytest -n auto -m "not single"

# Browser selection (pytest-playwright options)
pytest tests/ui --headed
pytest tests/ui --browser chromium --browser firefox
pytest tests/ui --browser-channel chrome       # or msedge

# Debug artifacts on failure
pytest tests/ui --tracing retain-on-failure --video retain-on-failure

# Replay a run with the same generated test data (seed is logged per test)
FAKER_SEED=123456 pytest tests/api/test_account_lifecycle.py
```

Screenshots, traces and videos are written to `test-results/`.

### Test Markers

`api` and `ui` are applied automatically based on the test folder.

| Marker | Description |
|--------|-------------|
| `smoke` | Smoke tests: one happy path per feature |
| `regression` | Full regression suite |
| `api` | API tests (no browser required) |
| `ui` | Browser-based UI tests |
| `contract` | Strict response schema checks |
| `negative` | Negative / error-handling tests |
| `single` | Must not run in parallel |
| `mobile` | Mobile-only tests |
| `quality_gate` | Quality gate tests |

---

## API Testing Approach

API tests use Playwright's `APIRequestContext`, the same tool as the UI tests. That means one dependency, one config, and API calls can set up UI tests directly.

### Layers

```
tests/api/*.py           what is tested: one behaviour per test, no HTTP details
      │
api/assertions.py        how the API reports outcomes (HTTP status + body responseCode)
      │
api/models/              Pydantic contracts for responses + request payload models
api/data/factories.py    test data builders (Faker)
      │
api/client/              one method per endpoint, plus raw request() for negative tests
      │
APIRequestContext        Playwright transport (session-scoped fixture)
```

- **Clients** (`ProductsClient`, `AccountsClient`) hide paths, methods and form encoding. `request()` stays public so negative tests can send any method or payload.
- **`ApiResponse`** is a snapshot of the exchange (method, URL, status, body, timing). Its string form is included in every assertion message, so a failure shows the full request and response without re-running the test.
- **Models** forbid unknown fields, so schema drift fails loudly. `assert_api_response(..., model=X)` validates the body and returns a typed object, which the tests then work with instead of raw dicts.

### Design decision: the status code is in the body

automationexercise.com answers **HTTP 200 for almost everything** and puts the real outcome in the body:

```json
{"responseCode": 405, "message": "This request method is not supported."}
```

A check like `response.ok` therefore proves nothing. `assert_api_response` checks the transport status and the body `responseCode` separately, and it's the only place in the framework that knows about this rule.

Exploring the API also showed that it **rejects unsupported methods in two different ways**: catalog endpoints return `200` + `responseCode: 405`, while account endpoints (and `PATCH` anywhere) return a real `HTTP 405` with a `{"detail": ...}` body. `test_unsupported_methods.py` pins both behaviours in one generated table.

### Test data lifecycle

- `new_user` builds a unique user (UUID-based email), so tests are safe to run in parallel and to re-run.
- `registered_user` creates the account through the API as a precondition.
- `cleanup_user` deletes every account a test registers after the test, whether it passed or failed. This includes accounts created through the UI.
- The Faker seed is random per test and logged, and `FAKER_SEED` replays it.

### Coverage

| Area | What is verified |
|------|------------------|
| Products / brands | Catalog content, unique IDs, known categories, product brands exist in `brandsList`, response time SLA |
| Search | Results match the term (name or category), case-insensitive, subset of catalog, empty/blank terms, missing parameter |
| Accounts | Create → read back field by field, update, delete, duplicate email, every required/optional field, wrong password does not modify or delete |
| Login | Valid credentials, wrong password, unknown email, email case sensitivity, missing parameters |
| Unsupported methods | Every endpoint × method combination |
| Contract | Strict schemas for all data payloads and error envelopes |

### API + UI together

- `tests/ui/test_login_with_api_user.py` creates the user through the API, so the UI test only exercises login.
- `tests/ui/test_sign_up.py` registers through the UI, then checks the result via the API and deletes the account.

---

## Project Structure

```
pytest-playwright-ui-api/
├── config.py               # Dynaconf settings loader
├── settings.toml           # Per-environment configuration
├── .secrets.toml           # Secrets (git-ignored, create manually)
├── requirements.txt        # pip dependencies
├── pyproject.toml          # Project metadata + pytest config
├── api/
│   ├── client/             # BaseApiClient + ProductsClient, AccountsClient
│   ├── models/             # Pydantic response contracts and request payloads
│   ├── data/factories.py   # Test data builders
│   └── assertions.py       # assert_api_response, assert_response_time
├── page_objects/
│   ├── page_creator.py     # PageCreator facade (injected via `ui` fixture)
│   └── *.py                # Individual page object classes
└── tests/
    ├── conftest.py         # Shared fixtures: API clients, test users, cleanup, faker seed
    ├── api/                # API tests
    └── ui/
        ├── conftest.py     # `ui` fixture (built on pytest-playwright's `page`)
        └── test_*.py       # UI and hybrid API+UI tests
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
