import click
from repository import init_repository,commit_repository


@click.group()
def cli():
    """WIT - a simple version control system"""
    pass


@cli.command()
def init():

    init_repository()
    """Initialize a new wit repository"""
    init_repository()


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
@click.argument("commit_id")
def checkout_command(commit_id):
    """Checkout a specific commit safely"""
    from repository import checkout
    checkout(commit_id)


if __name__ == "__main__":
    cli()

