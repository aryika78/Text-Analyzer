# Text Analyzer CLI

A Python-based Command Line Interface (CLI) that demonstrates core NLP preprocessing concepts with Rich-powered terminal output and structured JSON support.

This project is built for learning, interviews, and showcasing NLP fundamentals in a clean, production-style CLI.

---

## Features

* Tokenization

  * Sentence tokenization
  * Word tokenization
  * LLM token estimation with approximate cost

* Part-of-Speech (POS) Tagging

  * POS tags with human‑readable descriptions

* Named Entity Recognition (NER)

  * Entity detection (PERSON, ORG, GPE, etc.)
  * BIO tagging (B / I / O)

* Stemming

  * Porter
  * Snowball
  * Lancaster
  * Marks invalid stems clearly

* Lemmatization

  * POS‑aware lemmatization

* Stem vs Lemma Comparison

* Full Analysis Command

  * Combines all NLP steps with execution timing

* Disk I/O Support

  * Read input from text files
  * Save output as JSON

* JSON Output Mode

  * Machine‑readable output for pipelines and automation

* Unit Tested

  * Test coverage using Pytest

---

## Project Structure


text-analyzer/
├── app/
│   ├── __init__.py
│   ├── cli.py              # CLI commands (Typer + Rich)
│   ├── tokenizer.py        # Word, sentence & LLM tokenization
│   ├── pos_tagger.py       # POS tagging
│   ├── lemmatizer.py       # POS-aware lemmatization
│   ├── stemmer.py          # Porter, Snowball, Lancaster
│   └── ner.py              # NER + BIO tagging
├── tests/
│   ├── test_tokenizer.py
│   ├── test_pos.py
│   ├── test_lemmatizer.py
│   ├── test_stemmer.py
│   └── test_ner.py
├── requirements.txt
└── README.md


---

## Installation

### 1. Clone the repository

bash
git clone https://github.com/<your-username>/text-analyzer.git
cd text-analyzer


### 2. Create and activate a virtual environment

bash
python -m venv venv


*Windows*

bash
venv\Scripts\activate


*Linux / macOS*

bash
source venv/bin/activate


### 3. Install dependencies

bash
pip install -r requirements.txt


---

## CLI Usage

All commands are run using:

bash
python main.py <command> [OPTIONS]


### Tokenization

bash
python main.py tokenize "Dr. Strange opened a portal!"


Outputs sentence tokens, word tokens, and LLM token estimate with cost.

### POS Tagging

bash
python main.py pos "Naruto trained hard at the academy"


Displays token, POS tag, and description in a Rich table.

### Named Entity Recognition

bash
python main.py ner "Elon Musk founded SpaceX in California"


Outputs detected entities and BIO tags per token.

### Stemming

bash
python main.py stem "running studies easily happiness"


Shows Porter, Snowball, and Lancaster stems with invalid stems highlighted.

### Lemmatization

bash
python main.py lemmatize "The Avengers were fighting Thanos"


Performs POS‑aware lemmatization.

### Compare: Stemming vs Lemmatization

bash
python main.py compare "running studies better easily"


Includes comparison summary and winner per word.

### Full Analysis

bash
python main.py analyze "Tony Stark built Jarvis in Malibu"


Runs tokenization, POS, lemmas, stemming, NER, BIO tags, and execution time.

---

## Disk I/O

### Read input from a file

bash
python main.py analyze --file input.txt


Useful for large texts, batch processing, and automation workflows.

### Save output to a JSON file

bash
python main.py analyze --file input.txt --out result.json


Produces structured JSON suitable for APIs, ML pipelines, or dashboards.

### JSON output to terminal

bash
python main.py analyze "Tony Stark built Jarvis in Malibu" --json-output


Prints JSON directly to the terminal.

---

## Running Tests

bash
pytest -v


Covers tokenization, POS tagging, NER, stemming, and lemmatization.

---

## Why Disk I/O and JSON Output Matter

*Disk I/O*

* Enables real‑world usage for large text inputs
* Supports automation and batch NLP pipelines

*JSON Output*

* Standard data exchange format
* Easy integration with ML models, APIs, and dashboards

---

## Tech Stack

* Python 3.10+
* Typer (CLI framework)
* Rich (terminal UI)
* spaCy
* NLTK
* Pytest

---

## Status

* Mentor checklist items completed
* CLI UX polished
* Tests stable
* Repository ready for GitHub

---

## Author

*Aryika Patni*
Final Year | NLP & ML Intern
Focused on building clean, explainable, production‑style systems.