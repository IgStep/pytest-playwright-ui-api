## Pytest Playwright Test Automation Demo

### Introduction
This project has been created to showcase the basic structure for a test automation project based on pytest and playwright. 
It provides demo tests for web UI and API.

### SUT
Tests are provided for https://automationexercise.com/ - a practice website for Automation Engineers.

### Installation
1. Clone the repository
2. Install the requirements using pip or poetry
```bash
pip install -r requirements.txt
```
or
```bash
poetry install --no-root
```
### Project Configuration
For managing parameters of test environments, dynaconf package is used. Settings are stored in the `settings.toml` file.

### UI tests 
UI tests are created using widely used Page Object Model (POM) design pattern. To provide pages objects to the tests, fixture `ui` is used (please see `conftest.py` file).
`ui` fixture yields `PageCreator` class, which is a facade for all page objects. This approach keeps tests clean and readable.