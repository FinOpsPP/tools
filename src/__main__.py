"""primary code for the finopspp CLI"""
import os
import sys

import click

from finopspp.commands import utils
from finopspp.commands.init import group as init_group
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
    if not os.path.exists(config_path) and 'init' not in ctx.invoked_subcommand:
        click.secho(
            'Tool configuration does not exist. Please run `finopspp init`',
            err=True,
            fg='red'
        )
        sys.exit(1)
    if 'init' in ctx.invoked_subcommand:
        return

    # load up the config based on the path. This command can exit if an invalid config is found
    utils.load_config(config_path)

    # configure profiles and variables from what are found
    utils.profiles()
    utils.variables()

cli.add_command(init_group.init)
cli.add_command(init_group.validate, name='init-validate')
cli.add_command(info_group.info)
cli.add_command(generate_group.generate)
cli.add_command(specifications_group.specifications)
cli.add_command(inventory_group.inventory)
cli.add_command(variables_group.variables)


# include for those running script directly
# as a python module.
if __name__ == "__main__":
    cli() # pylint: disable=no-value-for-parameter
