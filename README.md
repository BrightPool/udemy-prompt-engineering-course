# Udemy Prompt Engineering Course

This is a Github repository for all of the source code used in the Udemy Prompt Engineering Course.

## Installation:

- Install gitleaks for secret scanning: `brew install gitleaks`
- Install pre-commit: `pip install pre-commit`
- Install pre-commit hooks: `pre-commit install`

## How to run Gitleaks to generate a report:

`gitleaks detect --source="." --report-path="gitleaks-report.json"`