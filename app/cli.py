import typer
from rich.console import Console
from rich.table import Table
from rich import box
import time
import json
from pathlib import Path
from app.tokenizer import sentence_tokens, word_tokens, llm_tokens
from app.pos_tagger import pos_tag_tokens
from app.lemmatizer import lemmatize_tokens
from app.ner import process_text, extract_entities_from_doc, generate_bio_tags_from_doc
from app.stemmer import stem_tokens

app = typer.Typer()
console = Console()

def read_input_text(text: str | None, file: str | None) -> str:
    if file:
        with open(file, "r", encoding="utf-8") as f:
            return f.read().strip()
    if text:
        return text
    raise typer.BadParameter("Provide either TEXT or --file")


# ----------------------------
# Helper Functions (UX SAFE)
# ----------------------------
def fmt_stem(stem, valid):
    return f"[green]{stem}[/green]" if valid else f"[red]{stem} ❌[/red]"

def highlight_entity(ent_text: str, ent_label: str):
    colors = {
        "PERSON": "bold magenta",
        "ORG": "bold green",
        "GPE": "bold cyan",
        "LOC": "bold yellow",
        "DATE": "bold blue"
    }
    return f"[{colors.get(ent_label,'bold white')}]{ent_text}[/{colors.get(ent_label,'bold white')}]"

def print_table(title, columns, rows):
    table = Table(
        title=f"[bold cyan]{title}[/bold cyan]",
        box=box.DOUBLE,
        show_lines=True,
        expand=True
    )
    for col in columns:
        table.add_column(col, style="bold white")
    for row in rows:
        table.add_row(*map(str, row))
    console.print(table)

# ----------------------------
# CLI Commands
# ----------------------------
@app.command()
def tokenize(text: str, json_output: bool = False):
    sentences = sentence_tokens(text)
    words = word_tokens(text)
    _, llm_count = llm_tokens(text)

    if json_output:
        console.print(json.dumps({
            "sentences": sentences,
            "words": words,
            "llm_tokens": llm_count,
            "llm_estimated_cost": round(0.00003 * llm_count, 6)
        }, indent=2))
        return

    print_table("Sentence Tokens", ["#", "Sentence"],
                [(i+1, s) for i, s in enumerate(sentences)])
    print_table("Word Tokens", ["#", "Token"],
                [(i+1, w) for i, w in enumerate(words)])

    console.print(f"[bold green]LLM Tokens:[/bold green] {llm_count}")
    console.print("[dim]~1 token ≈ ¾ word ≈ 4 characters[/dim]")

@app.command()
def pos(text: str, json_output: bool = False):
    tokens = word_tokens(text)
    tagged = pos_tag_tokens(tokens)

    if json_output:
        console.print(json.dumps([
            {"token": w, "pos": p, "description": d} for w, p, d in tagged
        ], indent=2))
        return

    print_table("POS Tagging", ["Token", "POS", "Description"], tagged)

@app.command()
def lemmatize(text: str, json_output: bool = False):
    tokens = word_tokens(text)
    tagged = pos_tag_tokens(tokens)
    tagged_simple = [(w, t) for w, t, _ in tagged]
    lemmas = lemmatize_tokens(tagged_simple)

    if json_output:
        console.print(json.dumps(lemmas, indent=2))
        return

    rows = [(i["token"], i["pos"], i["lemma"]) for i in lemmas]
    print_table("Lemmatization (POS-aware)", ["Token", "POS", "Lemma"], rows)

@app.command()
def stem(text: str, json_output: bool = False):
    tokens = word_tokens(text)
    stems = stem_tokens(tokens)

    if json_output:
        console.print(json.dumps(stems, indent=2))
        return

    rows = [
        (
            s["token"],
            fmt_stem(s["porter"], s["porter_valid"]),
            fmt_stem(s["snowball"], s["snowball_valid"]),
            fmt_stem(s["lancaster"], s["lancaster_valid"])
        )
        for s in stems
    ]
    print_table("Stemming Comparison",
                ["Token", "Porter", "Snowball", "Lancaster"], rows)

@app.command()
def ner(text: str, json_output: bool = False):
    doc = process_text(text)
    entities = extract_entities_from_doc(doc)
    bio_tags = generate_bio_tags_from_doc(doc)

    if json_output:
        console.print(json.dumps({
            "entities": entities,
            "bio_tags": [{"token": t, "tag": b} for t, b in bio_tags]
        }, indent=2))
        return

    if entities:
        rows = [(highlight_entity(e["text"], e["label"]), e["label"]) for e in entities]
        print_table("Named Entities", ["Entity", "Label"], rows)

    if bio_tags:
        print_table("BIO Tagging", ["Token", "BIO Tag"], bio_tags)

@app.command()
def analyze(
    text: str = typer.Argument(None),   # CHANGED
    file: Path = typer.Option(None, "--file", help="Path to input text file"),  # NEW
    json_output: bool = False,
    out: Path = typer.Option(None, "--out", help="Save output JSON to file")
):
    start_total = time.time()

    # ------------------------
    # NEW: Read input (CLI or file)
    # ------------------------
    text = read_input_text(text, file)   # NEW

    # ------------------------
    # Build result dictionary
    # ------------------------
    result = {}

    sentences = sentence_tokens(text)
    words = word_tokens(text)
    _, llm_count = llm_tokens(text)

    result["tokenization"] = {
        "sentences": sentences,
        "words": words,
        "llm_tokens": llm_count,
        "llm_estimated_cost": round(0.00003 * llm_count, 6)
    }

    tagged = pos_tag_tokens(words)
    tagged_simple = [(w, t) for w, t, _ in tagged]
    lemmas = lemmatize_tokens(tagged_simple)
    result["pos_lemmatization"] = lemmas

    stems = stem_tokens(words)
    result["stemming"] = stems

    doc = process_text(text)
    result["named_entities"] = extract_entities_from_doc(doc)
    result["bio_tags"] = [
        {"token": t, "tag": b}
        for t, b in generate_bio_tags_from_doc(doc)
    ]

    # ------------------------
    # Save JSON to file
    # ------------------------
    if out:
        out.write_text(json.dumps(result, indent=2), encoding="utf-8")

    # ------------------------
    # JSON-only output
    # ------------------------
    if json_output:
        console.print(json.dumps(result, indent=2))
        return

    # ------------------------
    # Rich UX output (unchanged)
    # ------------------------
    console.print(
        f"[bold cyan]📊 Full Text Analysis[/bold cyan]\n"
        f"[bold]Input:[/bold] {text}"
    )

    print_table(
        "Sentence Tokens",
        ["#", "Sentence"],
        [(i + 1, s) for i, s in enumerate(sentences)]
    )

    print_table(
        "Word Tokens",
        ["#", "Token"],
        [(i + 1, w) for i, w in enumerate(words)]
    )

    print_table(
        "POS + Lemmatization",
        ["Token", "POS", "Lemma"],
        [(i["token"], i["pos"], i["lemma"]) for i in lemmas]
    )

    print_table(
        "Stemming Comparison",
        ["Token", "Porter", "Snowball", "Lancaster"],
        [
            (
                s["token"],
                fmt_stem(s["porter"], s["porter_valid"]),
                fmt_stem(s["snowball"], s["snowball_valid"]),
                fmt_stem(s["lancaster"], s["lancaster_valid"]),
            )
            for s in stems
        ]
    )

    if result["named_entities"]:
        print_table(
            "Named Entities",
            ["Entity", "Label"],
            [
                (highlight_entity(e["text"], e["label"]), e["label"])
                for e in result["named_entities"]
            ]
        )

    if result["bio_tags"]:
        print_table(
            "BIO Tagging",
            ["Token", "BIO Tag"],
            [(b["token"], b["tag"]) for b in result["bio_tags"]]
        )

    console.print(
        f"[dim]⏱️ Total analysis time: "
        f"{round(time.time() - start_total, 3)}s[/dim]"
    )

if __name__ == "__main__":
    app()
