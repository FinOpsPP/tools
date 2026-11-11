"""Command file for all Init group commands"""
import os
import sys
import tomllib
from pathlib import Path

import click
from jinja2 import Environment, PackageLoader
from pydantic import ValidationError

from finopspp.models.tool_configuration import Configuration

Templates = PackageLoader('finopspp', 'templates')

@click.command()
@click.option(
    '--project-path',
    default='.',
    type=click.Path(resolve_path=True, path_type=Path),
    help='The location on your filesystem the configuration is written to. Defaults to current working directory'
)
def init(project_path):
    """Initialize the finopspp tools
    
    Creates a configuration file pointing to local copy of the
    Framework-Assessment. If git is installed on your system,
    it can also be used clone that project
    """
    # pull in template and specification files for given specification type
    env = Environment(loader=Templates, keep_trailing_newline=True)
    template = env.get_template('config.toml.j2')

    output = template.render(
        project_path=project_path,
    )

    home_directory = os.path.expanduser('~')
    config_dir = os.path.join(home_directory, '.finopspp')
    Path(config_dir).mkdir(parents=True, exist_ok=True)

    # finally, write README.md for the schemas
    # from the rendered output
    config_path = os.path.join(config_dir, , 'config.toml')
    with open(config_path, 'w', encoding='utf-8') as outfile:
        outfile.write(output)


@click.command()
def validate():
    """Validate finopspp configuration and setup"""
    model = Configuration

    home_directory = os.path.expanduser('~')
    config_path = os.path.join(home_directory, '.finopspp', 'config.toml')

    failed = False
    click.echo(f'Validating "{config_path}":')
    with open(config_path, 'rb') as toml_file:
        config_data = tomllib.load(toml_file)

    try:
        model.model_validate(config_data)
    except ValidationError as val_error:
        failed = True
        click.secho(
            f'Validation for "{config_path}" failed with --\n', fg='yellow'
        )
        click.secho(str(val_error) + '\n', err=True, fg='red')
    else:
        click.secho(
            f'Validation for "{config_path}" passed', fg='green'
            )

    if failed:
        sys.exit(1)
