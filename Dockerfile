FROM python:3.11-slim

WORKDIR /app

# NLTK data path
ENV NLTK_DATA=/usr/local/nltk_data

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 🔥 Install ALL POSSIBLE taggers explicitly
RUN python - <<EOF
import nltk
nltk.download("punkt", download_dir="/usr/local/nltk_data")
nltk.download("punkt_tab", download_dir="/usr/local/nltk_data")
nltk.download("wordnet", download_dir="/usr/local/nltk_data")
nltk.download("averaged_perceptron_tagger", download_dir="/usr/local/nltk_data")
nltk.download("averaged_perceptron_tagger_eng", download_dir="/usr/local/nltk_data")
EOF

# spaCy
RUN python -m spacy download en_core_web_sm

COPY . .

ENTRYPOINT ["python", "main.py"]
