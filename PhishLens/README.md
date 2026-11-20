# PhishLens — Explainable URL Threat Analyzer

A hackathon prototype that parses a submitted URL, checks suspicious URL patterns and lookalike domains, then produces an explainable 0–100 risk score.

**Safety:** PhishLens never opens, fetches, crawls or follows the submitted URL. This is a heuristic demonstration, not a threat-intelligence service. A low score does not certify a website as safe.

## Features
- URL parsing and normalization, including IDN-to-ASCII hostname conversion
- Checks for IP hosts, HTTP, embedded user-info, unusual ports, long URLs, deep subdomains, selected TLD patterns, shorteners, punycode, hyphens and sensitive-action keywords
- Lookalike checks against a small demo list of major brands
- Explainable weighted score, signal details and practical advice
- Browser dashboard and JSON API; no API keys or third-party runtime packages

## Run in VS Code on Windows
1. Open the PhishLens folder in VS Code.
2. Terminal → New Terminal.
3. Run: py -m venv .venv
4. Activate: .\.venv\Scripts\Activate.ps1 (or .venv\Scripts\activate.bat in Command Prompt).
5. Run: py -m pip install -r requirements.txt
6. Run: py app.py — app.py is the file to run.
7. Open http://127.0.0.1:5000

If PowerShell blocks activation, run Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass in that terminal, then activate again.

## Tests
Run: py -m unittest discover -s tests -v

## API
POST /api/analyze with JSON: {"url":"https://example.com/login"}. GET /health is the hosting health check.

## Public hosting
A Render Blueprint is provided at the repository root as render.yaml. Connect the GitHub repository to Render and create the Web Service. The Blueprint sets the service root directory to PhishLens.

The free hosting tier may sleep while idle. Do not submit credentials or sensitive URLs to a public demo.

## Scoring
Scores are capped at 100: 0–29 low, 30–59 medium, 60–100 high. Weights are demonstration values; tune them against a labelled validation dataset before real-world use. The brand list is limited and cannot establish whether a domain is legitimate.
