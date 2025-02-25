from click import command, option, pass_context, echo, style, secho
import json
import os
from pathlib import Path

@command()
@option('--help', is_flag=True, help='Show this message and exit.')
@pass_context
def help(ctx, help):
    if help:
        display_help()
        ctx.ensure_object(dict)
        ctx.obj['help'] = True
        return
    ctx.ensure_object(dict)
    ctx.obj['help'] = False
    display_help()

def display_help():
    """Display formatted help information from the help.jsonc file."""
    help_file_path = Path(__file__).parent.parent / "internal" / "help.jsonc"
    
    try:
        # Load the help information from the JSON file
        with open(help_file_path, 'r') as f:
            # Parse JSON with comments
            content = f.read()
            # Simple way to handle jsonc by removing comment lines
            lines = [line for line in content.split('\n') if not line.strip().startswith('//')]
            help_data = json.loads('\n'.join(lines))
        
        secho("DBDOCGEN - Database Documentation Generator", fg="green", bold=True)
        echo("\nAvailable commands:\n")
        
        for command_name, command_info in help_data.items():
            # Display command name and description
            secho(f"  {command_name}", fg="cyan", bold=True)
            echo(f"    {command_info['description']}")
            
            # Display command options if any
            if command_info.get('options'):
                echo("\n    Options:")
                for option_name, option_desc in command_info['options'].items():
                    echo(f"      {style(option_name, fg='yellow')}: {option_desc}")
            echo("")  # Add a blank line between commands
            
    except Exception as e:
        echo(f"Error loading help information: {str(e)}")
        echo("Please run 'dbdocgen help' for basic help information.")
