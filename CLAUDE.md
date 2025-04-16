# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Run Commands
- Install dependencies: `pip install -r requirements.txt` or `python install_pip_modules.py`
- Run all tests: `python manage.py test`
- Run app-specific tests: `python manage.py test app_name`
- Run single test: `python manage.py test app_name.tests.TestClass.test_method`
- IMPORTANT: Do NOT run `makemigrations`, `migrate`, or `runserver` commands - these are managed in production
- The codebase uses automation with Project/build/app_builder for code generation
- Project/build/make creates the dev environment
- run/jiva is the production git checkout

## Code Style Guidelines
- Follow PEP 8 conventions for Python code
- Use 4 spaces for indentation (no tabs)
- Import order: standard library → third-party → Django → local apps
- Class naming: CamelCase
- Function/variable naming: snake_case
- Model field names: snake_case
- Template variables: snake_case
- URL patterns: kebab-case
- Error handling: use try/except with specific exceptions
- Use Django's built-in logging for errors and warnings
- Include docstrings for classes and complex functions
- Type hints are encouraged for function parameters and return values


## Application 
- app_scrum is a scrum platform
- app_scrum has many modules
- app_scrum can deliver Project, Product, Solution, Consulting type of work