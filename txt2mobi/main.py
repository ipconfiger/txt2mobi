# coding=utf8

import sys
from txt2mobi.scaffold import op_init_project, generate_project, test_project
from utilities import start_server
import click


@click.group()
def cli():
    pass


@click.command()
def init():
    op_init_project()
    click.echo("project init successfull!")
    sys.exit(0)


@click.command()
@click.option('--title', default='', help='the pattern of chapter title')
def gen(title):
    generate_project(title)
    click.echo("project generated successfull!")
    sys.exit(0)


@click.command()
@click.option('--title', default='', help='the pattern of chapter title')
def test(title):
    test_project(title)
    click.echo("project test successfull!")
    sys.exit(0)


@click.command()
def trans():
    start_server()
    sys.exit(0)


def main():
    cli.add_command(init)
    cli.add_command(gen)
    cli.add_command(test)
    cli.add_command(trans)
    cli()



if __name__ == "__main__":
    main()
