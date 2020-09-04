import sys

from subprocrunner import SubprocessRunner

from cli_project_name._const import MODULE_NAME

from .common import print_result


class Test_cli:
    def test_help(self, tmpdir):
        runner = SubprocessRunner([sys.executable, "-m", MODULE_NAME, "-h"])
        runner.run()
        print_result(stdout=runner.stdout, stderr=runner.stderr)
        assert runner.returncode == 0
