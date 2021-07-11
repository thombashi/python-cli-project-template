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

    initialize_logger(name=f"{MODULE_NAME:s}", log_level=ctx.obj[Context.LOG_LEVEL])


@cmd.command(epilog=COMMAND_EPILOG)
@click.pass_context
def version(ctx):
    """
    Show version information
    """

    import envinfopy

    click.echo(
        envinfopy.dumps(
            ["cli_project_name"],
            format="markdown",
            verbosity_level=ctx.obj[Context.VERBOSITY_LEVEL],
        )
    )


@cmd.command(epilog=COMMAND_EPILOG)
@click.pass_context
@click.argument("filepaths", type=str, nargs=-1)
@click.option("--flag", "is_flag", is_flag=True, help="")
def subcmd_flag(ctx, filepaths, is_flag):
    """
    demo for flag options.
    """

    verbosity_level = ctx.obj[Context.VERBOSITY_LEVEL]

    for filepath in filepaths:
        click.echo(filepath)


@cmd.command(epilog=COMMAND_EPILOG)
@click.pass_context
@click.argument("choice", type=click.Choice(["hoge", "foo"]))
@click.option("--opt-choice", type=click.Choice(["hoge", "foo"]))
def subcmd_choice(ctx, choice: str, opt_choice: str):
    """
    demo for click.Choice.
    """

    verbosity_level = ctx.obj[Context.VERBOSITY_LEVEL]

    click.echo(choice)
    click.echo(opt_choice)


@cmd.command(epilog=COMMAND_EPILOG)
@click.argument("filepath", type=click.Path(exists=True))
@click.pass_context
def subcmd_path(ctx, filepath):
    """
    subcmd that takes a file as an input.
    """

    with open(filepath) as f:
        print(f.read())


if __name__ == "__main__":
    cmd()
