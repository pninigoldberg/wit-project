import click
from repository import init_repository


@cli.group()
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


if __name__ == "__main__":
    cli()

