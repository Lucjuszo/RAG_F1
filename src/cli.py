from retriever import Retriever
from llm import LocalLLM
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

console = Console()

def show_sources(chunks: list[dict]):
    table = Table(title="Context from Qdrant", box=box.SIMPLE_HEAVY, show_lines=True)
    table.add_column("#",       style="dim", width=3)
    table.add_column("Driver",  style="cyan")
    table.add_column("Score",   style="green", width=7)
    table.add_column("Snippet")
    for i, c in enumerate(chunks, 1):
        table.add_row(str(i), c["driver"], str(c["score"]),
                      c["text"][:200] + ("..." if len(c["text"]) > 200 else ""))
    console.print(table)

def ask(retriever: Retriever, llm: LocalLLM, query: str):
    console.print("\n[bold cyan]Searching in Qdrant...[/bold cyan]")
    chunks = retriever.search(query)

    if not chunks:
        console.print("[yellow]No matching snippets found.[/yellow]")
        return

    show_sources(chunks)

    context = "\n\n".join(
        f"[{c['driver']}]\n{c['text']}" for c in chunks
    )

    console.print("[bold cyan]Generating answer...[/bold cyan]")
    answer = llm.answer(context, query)

    console.print(Panel(answer, title="[bold green]Answer[/bold green]", border_style="green"))

def main():
    console.rule("[bold blue]F1 RAG - CLI[/bold blue]")
    console.print("[dim]Loading models...[/dim]\n")

    retriever = Retriever()
    llm       = LocalLLM()

    console.print("\n[bold]Ready! Enter a question or 'quit' to exit.[/bold]\n")

    while True:
        try:
            query = console.input("[bold yellow]❯ Question: [/bold yellow]").strip()
        except (KeyboardInterrupt, EOFError):
            break
        if not query:
            continue
        if query.lower() in ("quit", "exit", "q"):
            console.print("[dim]Goodbye![/dim]")
            break
        ask(retriever, llm, query)

if __name__ == "__main__":
    main()