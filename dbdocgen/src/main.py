import click
from dbdocgen.src.cmds.help import help
from dbdocgen.src.cmds.moreinfo.minfo import info

@click.group()
def cli():
    """dbdocgen: A tool for database documentation."""
    pass

cli.add_command(help)
cli.add_command(info)

def main():
    """Entry point for the application script"""
    cli()

if __name__ == '__main__':
    main()
