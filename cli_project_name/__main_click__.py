#!/usr/bin/env python3

from enum import Enum, unique

import click

from .__version__ import __version__
from ._const import MODULE_NAME, LogLevel
from ._logger import initialize_logger


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"], obj={})


@unique
class Context(Enum):
    LOG_LEVEL = 0
    VERBOSITY_LEVEL = 1


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
    ctx.obj[Context.LOG_LEVEL] = LogLevel.INFO if log_level is None else log_level
    ctx.obj[Context.VERBOSITY_LEVEL] = verbosity_level


@cmd.command()
@click.pass_context
@click.argument("filepaths", type=str, nargs=-1)
@click.option("--flag", "is_flag", is_flag=True, help="")
def subcmd1(ctx, filepaths, is_flag):
    log_level = ctx.obj[Context.LOG_LEVEL]
    verbosity_level = ctx.obj[Context.VERBOSITY_LEVEL]

    initialize_logger(name="{:s} subcmd1".format(MODULE_NAME), log_level=ctx.obj[Context.LOG_LEVEL])

    for filepath in filepaths:
        click.echo(filepath)


@cmd.command()
@click.pass_context
@click.argument("choices", type=click.Choice(["hoge", "foo"]))
def subcmd2(ctx, choice):
    log_level = ctx.obj[Context.LOG_LEVEL]
    verbosity_level = ctx.obj[Context.VERBOSITY_LEVEL]

    initialize_logger(name="{:s} subcmd2".format(MODULE_NAME), log_level=ctx.obj[Context.LOG_LEVEL])

    click.echo(choice)


if __name__ == "__main__":
    cmd()
