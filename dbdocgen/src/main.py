import click
from .cmds.help import help
from .cmds.moreinfo.minfo import info
from .cmds.v.version import version
@click.group()
def cli():
    """dbdocgen: A tool for database documentation."""
    pass

cli.add_command(help)
cli.add_command(info)
cli.add_command(version)
def main():
    """Entry point for the application script"""
    cli()

if __name__ == '__main__':
    main()
