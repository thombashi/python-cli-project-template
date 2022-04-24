"""
.. codeauthor:: NAME <EMAIL>
"""

import argparse
import sys
from textwrap import dedent
from typing import Tuple

from .__version__ import __version__
from ._const import MODULE_NAME
from ._logger import LogLevel, initialize_logger, logger


def parse_option() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=dedent(
            """\
            Issue tracker: https://github.com/username/package/issues
            """
        ),
    )
    parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("-v", "--verbose", dest="verbosity_level", action="count", default=0)

    use_stdin, found_stdin_specifier = is_use_stdin()
    if not use_stdin or found_stdin_specifier:
        parser.add_argument(
            "values",
            nargs="+",
            help="'-' for read from the standard input.",
        )

    group = parser.add_argument_group("Group")  # type: ignore
    group.add_argument(
        "--choices",
        choices=["a", "b"],
        default="a",
        help="defaults to %(default)s",
    )
    group.add_argument(
        "--flag",
        action="store_true",
        default=False,
        help="",
    )

    loglevel_dest = "log_level"
    group = parser.add_mutually_exclusive_group()  # type: ignore
    group.add_argument(
        "--debug",
        dest=loglevel_dest,
        action="store_const",
        const=LogLevel.DEBUG,
        default=LogLevel.INFO,
        help="for debug print.",
    )
    group.add_argument(
        "--quiet",
        dest=loglevel_dest,
        action="store_const",
        const=LogLevel.QUIET,
        default=LogLevel.INFO,
        help="suppress execution log messages.",
    )

    return parser.parse_args()


def is_use_stdin() -> Tuple[bool, bool]:
    if sys.stdin.isatty():
        return (False, False)

    found_stdin_specifier = "-" in sys.argv[1:]

    return (len(sys.argv) == 1 or found_stdin_specifier, found_stdin_specifier)


def main() -> int:
    ns = parse_option()

    initialize_logger(name=MODULE_NAME, log_level=ns.log_level)

    use_stdin, found_stdin_specifier = is_use_stdin()

    if not use_stdin and not found_stdin_specifier:
        logger.info("CLI tool template for argparse")
    else:
        logger.info(f"input from stdin: {sys.stdin.read()}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
