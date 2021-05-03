#!/usr/bin/env python3

from enum import Enum, auto, unique
from textwrap import dedent

import click

from .__version__ import __version__
from ._const import MODULE_NAME
from ._logger import LogLevel, initialize_logger


COMMAND_EPILOG = dedent(
    """\
    Issue tracker: https://github.com/:owner/:repo/issues
    """
)
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"], obj={})


@unique
class Context(Enum):
    LOG_LEVEL = auto()
    VERBOSITY_LEVEL = auto()


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__, message="%(prog)s %(version)s")
@click.option("--debug", "log_level", flag_value=LogLevel.DEBUG, help="For debug print.")
@click.option(
    "-q",
    "--quiet",
    "log_level",
    flag_value=LogLevel.QUIET,
    help="Suppress execution log messages.",
)
@click.option("-v", "--verbose", "verbosity_level", count=True)
@click.pass_context
def cmd(ctx, log_level: str, verbosity_level: int):
    """
    common cmd help
    """

    ctx.obj[Context.LOG_LEVEL] = LogLevel.INFO if log_level is None else log_level
    ctx.obj[Context.VERBOSITY_LEVEL] = verbosity_level

    initialize_logger(name="{:s}".format(MODULE_NAME), log_level=ctx.obj[Context.LOG_LEVEL])


@cmd.command(epilog=COMMAND_EPILOG)
@click.pass_context
def version(ctx):
    """
    Show version information
    """

    import envinfopy

    click.echo(envinfopy.dumps(["cli_project_name"], "markdown"))


@cmd.command(epilog=COMMAND_EPILOG)
@click.pass_context
@click.argument("filepaths", type=str, nargs=-1)
@click.option("--flag", "is_flag", is_flag=True, help="")
def subcmd1(ctx, filepaths, is_flag):
    """
    subcmd1 help
    """

    verbosity_level = ctx.obj[Context.VERBOSITY_LEVEL]

    for filepath in filepaths:
        click.echo(filepath)


@cmd.command(epilog=COMMAND_EPILOG)
@click.pass_context
@click.argument("choices", type=click.Choice(["hoge", "foo"]))
def subcmd2(ctx, choice):
    """
    subcmd2 help
    """

    verbosity_level = ctx.obj[Context.VERBOSITY_LEVEL]

    click.echo(choice)


@cmd.command(epilog=COMMAND_EPILOG)
@click.argument("filepath", type=click.Path(exists=True))
@click.pass_context
def subcmdpath(ctx, filepath):
    """
    subcmd that takes a file as an input.
    """

    with open(filepath) as f:
        print(f.read())


if __name__ == "__main__":
    cmd()
