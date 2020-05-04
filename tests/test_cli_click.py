import pytest
from click.testing import CliRunner

from cli_project_name.__main_click__ import cmd


class Test_click:
    @pytest.mark.parametrize(
        ["options", "expected"], [[["-h"], 0], [["subcmd1", "-h"], 0], [["subcmd2", "-h"], 0],],
    )
    def test_help(self, options, expected):
        runner = CliRunner()
        result = runner.invoke(cmd, options)
        assert result.exit_code == expected
