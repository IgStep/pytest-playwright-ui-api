# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

pytest + Playwright test automation framework for UI and API testing against [automationexercise.com](https://automationexercise.com). Uses the Page Object Model (POM) pattern with a PageCreator facade.

## Commands

### Install dependencies
```bash
# pip
pip install -r requirements.txt
python -m playwright install --with-deps

# Poetry
poetry install
poetry run playwright install --with-deps
```

### Run tests
```bash
# All tests (headless, screenshots on failure)
pytest tests

# API only (no browser) / UI only
pytest tests/api -n auto
pytest tests/ui

# Single test by name
pytest tests/api/test_verify_login.py::test_verify_login_with_valid_credentials

# By marker
pytest -m smoke
pytest -m "api and negative"

# Parallel execution (skip tests marked `single`)
pytest -n auto -m "not single"

# Browser selection: pytest-playwright's built-in options
pytest tests/ui --headed --browser firefox
pytest tests/ui --browser-channel chrome
```

### Linting
```bash
ruff check .
```

## Code Style

Use comments sparingly — only for complex or non-obvious logic.

## Architecture

### Configuration
- `settings.toml` holds per-environment settings (`[dev]`, `[qa]`, `[uat]`, `[prod]`). Tests use `settings.qa.base_url`.
- `config.py` loads settings via dynaconf. Secrets go in `.secrets.toml` (git-ignored). Override via `DYNACONF_` env vars.

### Page Object Model
- `page_objects/page_creator.py` — **PageCreator** is a facade injected into tests via the `ui` fixture. Tests call `ui.main_page()`, `ui.products_page()`, etc. rather than instantiating page objects directly.
- Each page class (e.g., `page_objects/main.py`) exposes selectors as properties (Playwright locators) and navigation methods like `open()`.

### API layer (`api/`)
- `api/client/` — `BaseApiClient.request()` wraps `APIRequestContext.fetch` and returns an `ApiResponse` snapshot. `ProductsClient` / `AccountsClient` expose one method per endpoint; tests never build paths or form payloads themselves.
- `api/models/responses.py` — Pydantic response contracts (`extra="forbid"`). `api/models/user.py` — `UserData` request payload; `expected_user_detail()` maps request field names to the names the API returns.
- `api/assertions.py` — `assert_api_response(resp, code=, message=, http_status=, model=)`. The API returns HTTP 200 for most errors with the real status in the body `responseCode`; always assert through this helper, not `response.ok`.
- `api/data/factories.py` — `build_user(faker, **overrides)`; emails are UUID-based for parallel safety.
- The `api_context` base URL must end with `/api/` and client paths must be relative (no leading slash). Otherwise Playwright resolves them against the site root.

### Fixtures
| Fixture | Scope | Where | Purpose |
|---------|-------|-------|---------|
| `api_context` | session | `tests/conftest.py` | Playwright `APIRequestContext` pointed at `/api/` |
| `products_client`, `accounts_client` | session | `tests/conftest.py` | API clients |
| `new_user` | function | `tests/conftest.py` | Unregistered `UserData` |
| `registered_user` | function | `tests/conftest.py` | User created via API, deleted after the test |
| `cleanup_user` | function | `tests/conftest.py` | Callable; registers a user for deletion after the test |
| `faker_seed` | function | `tests/conftest.py` | Random, logged seed for the faker plugin's `faker` (override with `FAKER_SEED`) |
| `ui` | function | `tests/ui/conftest.py` | `PageCreator` built on pytest-playwright's `page` |

Browser, context and page come from pytest-playwright. Don't redefine them, or `--screenshot`/`--tracing`/`--video` stop working.

### Test Markers
- `api` / `ui` — applied automatically from the test folder
- `smoke` — smoke tests
- `regression` — full regression suite
- `contract` — strict schema checks
- `negative` — negative / error-handling tests
- `single` — must not run in parallel
- `mobile` — mobile-only tests
- `quality_gate` — quality gate tests

## CI/CD

- `.github/workflows/ruff_check.yml` — runs `ruff check` on every push
- `.github/workflows/run_all_tests.yml` — runs full test suite on manual trigger (`workflow_dispatch`)