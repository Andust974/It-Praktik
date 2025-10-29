import typer

app = typer.Typer(help="IT Praktik CLI")

@app.command()
def hello(name: str = "world"):
    """Demo command
    """
    typer.echo(f"Hello, {name}!")

if __name__ == "__main__":
    app()
