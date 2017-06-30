import click

from config import Config
from template import render


@click.group()
def main():

    """tbd: the CloudFormation tool"""


@main.command(name='print')
@click.argument('path', type=click.Path(exists=True))
def c_print(path):

    """render and print a template"""

    config = Config()
    tmpl = render(path, config.base_dir)
    click.echo(tmpl)
