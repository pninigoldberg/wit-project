import click
from repository import init_repository,commit_repository
from repository import status_repository


@click.group()
def cli():
    """WIT - a simple version control system"""
    pass


@cli.command()
def init():

    init_repository()
    """Initialize a new wit repository"""



@cli.command()
@click.argument("path")
def add(path):
    """Add a file or directory to the staging area"""
    print(f"ADD COMMAND CALLED: {path}")  # לבדיקה
    from repository import add_to_staging
    add_to_staging(path)


@cli.command()
@click.argument("message")
def commit(message):
    commit_repository(message)


@cli.command()
def status():
    """Show the status of the repository"""
    s = status_repository()  # קורא לפונקציה מה-repository.py

    # הדפסת קבצים ב-staged
    print("STAGED:")
    if s["staged"]:
        for f in s["staged"]:
            print(f"  {f}")
    else:
        print("  (none)")

    # הדפסת קבצים modified
    print("\nMODIFIED:")
    if s["modified"]:
        for f in s["modified"]:
            print(f"  {f}")
    else:
        print("  (none)")

    # הדפסת קבצים untracked
    print("\nUNTRACKED:")
    if s["untracked"]:
        for f in s["untracked"]:
            print(f"  {f}")
    else:
        print("  (none)")



@cli.command()
@click.argument("commit_id")
def checkout_command(commit_id):
    """Checkout a specific commit safely"""
    from repository import checkout
    checkout(commit_id)


if __name__ == "__main__":
    cli()

