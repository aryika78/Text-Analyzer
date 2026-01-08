# 📝 Text Analyzer CLI

A powerful **Python-based Command Line Interface (CLI)** that demonstrates **core NLP preprocessing concepts** with beautiful Rich-based output and structured JSON support.

---

## 🚀 Features

### 🔤 Tokenization

* Sentence tokens
* Word tokens
* LLM token estimation with cost

### 🏷️ Part-of-Speech (POS) Tagging

* POS tags with human-readable descriptions

### 🎯 Named Entity Recognition (NER)

* Entity detection (PERSON, ORG, GPE, etc.)
* BIO tagging (B- / I- / O)

### 🌿 Stemming

* Porter
* Snowball
* Lancaster
* Invalid stems marked with ❌

### 🌳 Lemmatization

* POS-aware lemmatization

### 🔬 Stem vs Lemma Comparison

### 📊 Full Analysis Command

* Combines all NLP steps
* Rich tables + timing

### 📁 Disk I/O Support

* Read input from text files
* Save output as JSON files

### 📦 JSON Output Mode

* Machine-readable output for pipelines

### 🧪 Unit Tested

* All tests passing with Pytest

---

## 📁 Project Structure

```text
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
```

---

## ⚙️ Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/<your-username>/text-analyzer.git
cd text-analyzer
```

### 2️⃣ Create and activate virtual environment

```bash
python -m venv venv
```

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🧠 CLI Usage

All commands are run using:

```bash
python main.py <command> [OPTIONS]
```

---

### 🔤 Tokenization

```bash
python main.py tokenize "Dr. Strange opened a portal!"
```

✔ Sentence tokens
✔ Word tokens
✔ LLM token estimate + cost

---

### 🏷️ POS Tagging

```bash
python main.py pos "Naruto trained hard at the academy"
```

Displays token, POS tag, and description in a Rich table.

---

### 🎯 Named Entity Recognition

```bash
python main.py ner "Elon Musk founded SpaceX in California"
```

* Detected entities
* BIO tags per token

---

### 🌿 Stemming

```bash
python main.py stem "running studies easily happiness"
```

Shows all three stemming algorithms with ❌ for invalid stems.

---

### 🌳 Lemmatization

```bash
python main.py lemmatize "The Avengers were fighting Thanos"
```

POS-aware lemmatization output.

---

### 🔬 Compare: Stemming vs Lemmatization

```bash
python main.py compare "running studies better easily"
```

Includes:

* Winner per word
* Summary statistics

---

### 📊 Full Analysis

```bash
python main.py analyze "Tony Stark built Jarvis in Malibu"
```

Combines:

* Tokenization
* POS + Lemmas
* Stemming
* NER
* BIO tags
* Execution time

---

### 📁 Read Input from File (Disk I/O)

```bash
python main.py analyze --file input.txt
```

✔ Useful for large texts
✔ Enables batch processing
✔ Real-world pipeline friendly

---

### 💾 Save Output to JSON File

```bash
python main.py analyze --file input.txt --out result.json
```

* Output is pure JSON
* Can be consumed by APIs, ML pipelines, or dashboards
* You may use any filename, not just `result.json`

---

### 🧾 JSON Output Mode

```bash
python main.py analyze "Tony Stark built Jarvis in Malibu" --json-output
```

Prints structured JSON directly to the terminal.

---

## 🧪 Running Tests

```bash
pytest -v
```

✅ All tests passing
✅ Covers tokenization, POS, NER, stemming, lemmatization

---

## 📌 Tech Stack

* Python 3.10+
* Typer (CLI framework)
* Rich (terminal UI)
* spaCy
* NLTK
* Pytest

---

## Author

**Aryika Patni**
