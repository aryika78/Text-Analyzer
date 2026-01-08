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
    llm_cost = round(0.00003 * llm_count, 6)  # Estimated cost

    if json_output:
        console.print(json.dumps({
            "sentences": sentences,
            "words": words,
            "llm_tokens": llm_count,
            "llm_estimated_cost": llm_cost
        }, indent=2))
        return

    # ------------------------
    # Rich output
    # ------------------------
    print_table("Sentence Tokens", ["#", "Sentence"],
                [(i+1, s) for i, s in enumerate(sentences)])
    print_table("Word Tokens", ["#", "Token"],
                [(i+1, w) for i, w in enumerate(words)])

    console.print(f"[bold green]LLM Tokens:[/bold green] {llm_count}")
    console.print(f"[bold green]Estimated LLM Cost:[/bold green] ${llm_cost}")
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
def compare(
    text: str = typer.Argument(None, help="Input text to compare stemming vs lemmatization"),
    file: Path = typer.Option(None, "--file", help="Path to input text file"),  # optional
    json_output: bool = False,
    out: Path = typer.Option(None, "--out", help="Save comparison output JSON to file")
):
    """
    Compare Stemming vs Lemmatization for the given text.

    - If `text` is provided, it will be analyzed directly.
    - If `--file` is provided, text will be read from the file.
    - `--json-output` prints the JSON result instead of tables.
    - `--out` saves the JSON result to the specified file.
    """

    # ------------------------
    # Read text from file if provided
    # ------------------------
    if file:
        text = file.read_text(encoding="utf-8")

    # ------------------------
    # Processing
    # ------------------------
    tokens = word_tokens(text)
    tagged = pos_tag_tokens(tokens)
    tagged_simple = [(w, t) for w, t, _ in tagged]

    lemmas = lemmatize_tokens(tagged_simple)
    lemma_map = {item["token"]: item for item in lemmas}

    stems = stem_tokens(tokens)

    rows = []
    lemma_wins = 0
    stem_wins = 0
    stem_valid_words = set()
    lemma_valid_words = set()

    # ------------------------
    # Comparison logic
    # ------------------------
    for s in stems:
        word = s["token"]
        porter = s["porter"]
        porter_valid = s["porter_valid"]

        lemma = lemma_map[word]["lemma"]
        lemma_valid = lemma_map[word]["lemma_valid"]

        # STRICT winner logic
        if porter == lemma:
            winner = "TIE"
        elif lemma_valid and not porter_valid:
            winner = "LEMMA ✅"
            lemma_wins += 1
        elif porter_valid and not lemma_valid:
            winner = "STEM ✅"
            stem_wins += 1
        else:
            winner = "LEMMA ✅"
            lemma_wins += 1

        # WordNet validity (stats only)
        if porter_valid:
            stem_valid_words.add(porter)
        if lemma_valid:
            lemma_valid_words.add(lemma)

        rows.append((word, porter, lemma, winner))

    # ------------------------
    # Save JSON output if requested
    # ------------------------
    result = {
        "input": text,
        "comparison": [
            {"token": r[0], "porter": r[1], "lemma": r[2], "winner": r[3]}
            for r in rows
        ],
        "summary": {
            "lemma_wins": lemma_wins,
            "stem_wins": stem_wins,
            "stem_valid_words": list(stem_valid_words),
            "lemma_valid_words": list(lemma_valid_words),
            "overall_winner": (
                "Lemmatization 🏆" if lemma_wins > stem_wins else
                "Stemming 🏆" if stem_wins > lemma_wins else
                "Tie 🤝"
            )
        }
    }

    if json_output:
        console.print(json.dumps(result, indent=2))
        if out:
            out.write_text(json.dumps(result, indent=2), encoding="utf-8")
        return

    # ------------------------
    # Rich CLI output
    # ------------------------
    console.print("[bold cyan]⚖️ Stemming vs Lemmatization Comparison[/bold cyan]")
    console.print(f"[bold]Input:[/bold] {text}")

    print_table(
        "🔬 Stemming vs Lemmatization",
        ["Word", "Porter Stem", "Lemma", "Winner"],
        rows
    )

    console.print("\n[bold]⚖️ Decision Summary[/bold]")
    console.print(f"  [cyan]Lemma wins:[/cyan] {lemma_wins}")
    console.print(f"  [green]Stem wins:[/green] {stem_wins}")

    overall = "Lemmatization 🏆" if lemma_wins > stem_wins else "Stemming 🏆" if stem_wins > lemma_wins else "Tie 🤝"
    console.print(f"\n[bold green]🏆 Overall Winner:[/bold green] {overall}")

    console.print("\n[bold]📊 Valid English Words (WordNet)[/bold]")
    console.print(f"  [green]Porter stems found:[/green] {len(stem_valid_words)}")
    console.print(f"  [cyan]Lemmas found:[/cyan] {len(lemma_valid_words)}")

    # ------------------------
    # Save to file if requested
    # ------------------------
    if out:
        out.write_text(json.dumps(result, indent=2), encoding="utf-8")


@app.command()
def analyze(
    text: str = typer.Argument(None),
    file: Path = typer.Option(None, "--file", help="Path to input text file"),
    json_output: bool = False,
    out: Path = typer.Option(None, "--out", help="Save output JSON to file")
):
    start_total = time.time()

    # ------------------------
    # Read input (CLI or file)
    # ------------------------
    text = read_input_text(text, file)

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

    # ------------------------
    # NEW: Stemming vs Lemmatization comparison
    # ------------------------
    lemma_map = {l["token"]: l for l in lemmas}
    comparison_rows = []

    lemma_wins = 0
    stem_wins = 0

    for s in stems:
        token = s["token"]
        porter = s["porter"]
        porter_valid = s["porter_valid"]

        lemma = lemma_map[token]["lemma"]
        lemma_valid = lemma_map[token]["lemma_valid"]

        if porter == lemma:
            winner = "TIE"
        elif lemma_valid and not porter_valid:
            winner = "LEMMA"
            lemma_wins += 1
        elif porter_valid and not lemma_valid:
            winner = "STEM"
            stem_wins += 1
        else:
            winner = "LEMMA"
            lemma_wins += 1

        comparison_rows.append({
            "token": token,
            "porter": porter,
            "lemma": lemma,
            "winner": winner
        })

    overall_winner = (
        "Lemmatization"
        if lemma_wins > stem_wins
        else "Stemming"
        if stem_wins > lemma_wins
        else "Tie"
    )

    result["stem_vs_lemma_comparison"] = {
        "rows": comparison_rows,
        "lemma_wins": lemma_wins,
        "stem_wins": stem_wins,
        "overall_winner": overall_winner
    }

    # ------------------------
    # NER + BIO tagging
    # ------------------------
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
    # Rich UX output
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

    # ------------------------
    # NEW: Compare table output
    # ------------------------
    print_table(
        "Stemming vs Lemmatization (Winner-based)",
        ["Token", "Porter Stem", "Lemma", "Winner"],
        [
            (r["token"], r["porter"], r["lemma"], r["winner"])
            for r in result["stem_vs_lemma_comparison"]["rows"]
        ]
    )

    console.print(
        f"[bold green]🏆 Overall Winner:[/bold green] "
        f"{result['stem_vs_lemma_comparison']['overall_winner']}"
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
