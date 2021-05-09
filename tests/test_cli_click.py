import pytest
from click.testing import CliRunner

from cli_project_name.__main_click__ import cmd


class Test_click:
    @pytest.mark.parametrize(
        ["options", "expected"],
        [
            [["-h"], 0],
            [["subcmd-flag", "-h"], 0],
            [["subcmd-choice", "-h"], 0],
            [["subcmd-path", "-h"], 0],
        ],
    )
    def test_help(self, options, expected):
        runner = CliRunner()
        result = runner.invoke(cmd, options)
        assert result.exit_code == expected


class Test_click_version:
    def test_smoke(self):
        runner = CliRunner()
        result = runner.invoke(cmd, ["version"])
        assert result.exit_code == 0
        assert len(result.stdout) > 30
