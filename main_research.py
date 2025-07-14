import asyncio
from functools import wraps

import typer
from prompt_toolkit import PromptSession
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from agents.research_agent import deep_research, generate_feedback, write_final_report


app = typer.Typer()
console = Console()
session = PromptSession()


def coro(func):
    """Decorator to allow async Typer commands."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))
    return wrapper


async def async_prompt(message: str, default: str = "") -> str:
    """Async wrapper for prompt_toolkit."""
    return await session.prompt_async(message)


@app.command()
@coro
async def main(
    concurrency: int = typer.Option(
        default=2,
        help="Number of concurrent tasks, depending on your API rate limits.",
    ),
):
    """Deep Research CLI Tool."""
    console.print(
        Panel.fit(
            "[bold blue]Deep Research Assistant[/bold blue]\n[dim]An AI-powered research tool[/dim]"
        )
    )

    # Prompt user for inputs
    query = await async_prompt("\n🔍 What would you like to research? ")
    console.print()

    breadth = int((await async_prompt("📊 Research breadth (recommended 2-10) [4]: ")) or "4")
    console.print()

    depth = int((await async_prompt("🔍 Research depth (recommended 1-5) [2]: ")) or "2")
    console.print()

    console.print("\n[yellow]Creating research plan...[/yellow]")
    follow_up_questions = await generate_feedback(query)

    console.print("\n[bold yellow]Follow-up Questions:[/bold yellow]")
    answers = []
    for i, question in enumerate(follow_up_questions, 1):
        console.print(f"\n[bold blue]Q{i}:[/bold blue] {question}")
        answer = await async_prompt("➤ Your answer: ")
        answers.append(answer)
        console.print()

    combined_query = (
        f"\nInitial Query: {query}\n"
        "Follow-up Questions and Answers:\n"
        f"{chr(10).join(f'Q: {q} A: {a}' for q, a in zip(follow_up_questions, answers))}"
    )

    # Execute research with progress feedback
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("[yellow]Researching your topic...[/yellow]", total=None)
        research_results = await deep_research(
            query=combined_query,
            breadth=breadth,
            depth=depth,
            concurrency=concurrency,
        )
        progress.remove_task(task)

        console.print("\n[yellow]Learnings:[/yellow]")
        for learning in research_results["learnings"]:
            rprint(f"• {learning}")

        task = progress.add_task("Writing final report...", total=None)
        report = await write_final_report(
            prompt=combined_query,
            learnings=research_results["learnings"],
            visited_urls=research_results["visited_urls"],
        )
        progress.remove_task(task)

        console.print("\n[bold green]Research Complete![/bold green]")
        console.print("\n[yellow]Final Report:[/yellow]")
        console.print(Panel(report, title="Research Report"))

        console.print("\n[yellow]Sources:[/yellow]")
        for url in research_results["visited_urls"]:
            rprint(f"• {url}")

        with open("output.md", "w") as file:
            file.write(report)
        console.print("\n[dim]Report has been saved to output.md[/dim]")


def run():
    """CLI synchronous entry point."""
    asyncio.run(app())


if __name__ == "__main__":
    asyncio.run(app())
