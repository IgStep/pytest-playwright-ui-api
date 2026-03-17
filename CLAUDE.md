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
# All tests (headed, screenshots on failure)
pytest tests

# Single test file
pytest tests/test_api.py

# Single test by name
pytest tests/test_api.py::test_get_product_list

# By marker
pytest -m smoke
pytest -m "not single"

# Parallel execution (skip tests marked `single`)
pytest -n auto -m "not single"

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

### Fixtures (`tests/conftest.py`)
| Fixture | Scope | Purpose |
|---------|-------|---------|
| `browser` | session | Headless browser instance |
| `context` | function | Isolated browser context per test |
| `ui` | function | `PageCreator` instance for UI tests |
| `api` | session | Playwright `APIRequestContext` pointed at `/api` |
| `faker` | function | Faker instance for test data |

### Test Markers
- `smoke` — smoke tests
- `single` — must not run in parallel
- `mobile` — mobile-only tests
- `quality_gate` — quality gate tests

## CI/CD

- `.github/workflows/ruff_check.yml` — runs `ruff check` on every push
- `.github/workflows/run_all_tests.yml` — runs full test suite on manual trigger (`workflow_dispatch`)