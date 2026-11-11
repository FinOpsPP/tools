"""primary code for the finopspp CLI"""
import os
import sys
import tomllib
from importlib import util

import click

from finopspp.commands import utils
from finopspp.commands.info import group as info_group
from finopspp.commands.generate import group as generate_group
from finopspp.commands.specifications import group as specifications_group
from finopspp.commands.inventory import group as inventory_group
from finopspp.commands.variables import group as variables_group


@click.group(cls=utils.ClickGroup)
@click.pass_context
def cli(ctx):
    """FinOps++ administration tool"""
    home_directory = os.path.expanduser('~')
    config_path = os.path.join(home_directory, '.finopspp', 'config.toml')
    if not os.path.exists(config_path) and ctx.invoked_subcommand != 'init':
        click.secho(
            'Tool configuration does not exist. Please run `finopspp init`',
            err=True,
            fg='red'
        )
        sys.exit(1)

    with open(config_path, 'rb') as toml_file:
        config = tomllib.load(toml_file)

    framework = config.get('framework')
    if not config.get('framework'):
        click.secho(
            f'Missing `framework` section in {config_path}. Exiting!',
            err=True,
            fg='red'
        )
        sys.exit(1)

    project_path = framework.get('project_path')
    if not project_path and not os.path.exists(project_path):
        click.secho(
            f'''Configuration requires a valid `project_path` field.

            Either the field was not included, or the path could not be found
            on your filesystem. Please check {config_path} to double check this
            field
            ''',
            err=True,
            fg='red'
        )
        sys.exit(1)

    sys.path.insert(0, project_path)

    if any([
        util.find_spec('specifications.actions') is None,
        util.find_spec('specifications.capabilities') is None,
        util.find_spec('specifications.domains') is None,
        util.find_spec('specifications.variables') is None
    ]):
        click.secho(
            'Your specifications directory appears to be missing one or more needed subdirectories. Exiting!',
            err=True,
            fg='red'
        )
        sys.exit(1)

    # configure profiles and variables from what are found
    utils.profiles()
    utils.variables()


cli.add_command(info_group.info)
cli.add_command(generate_group.generate)
cli.add_command(specifications_group.specifications)
cli.add_command(inventory_group.inventory)
cli.add_command(variables_group.variables)


# include for those running script directly
# as a python module.
if __name__ == "__main__":
    cli() # pylint: disable=no-value-for-parameter
