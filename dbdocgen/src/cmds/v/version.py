from click import command, option, pass_context, echo, style, secho

from pathlib import Path
from dbdocgen import __version__


@command()
@option('--version', is_flag=True, help='Show the version of the project.')
@pass_context
def version(ctx, version):
    if version:
        echo(f"DBDocgen version {__version__}")
    else:
        echo(f"DBDocgen version {__version__}")