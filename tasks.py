from sys import platform
from invoke import task


COLOR_OUTPUT = platform == 'linux'


def make_cmd(env: str) -> str:
    return f"tox -e {env} -r"

@task
def exec_test_suite_specific_requirement_denmark_tester(c):
    """execute testing with pip-requires.txt and demo tester"""
    c.run(
        make_cmd("exec-test-suite-specific-requirement-denmark-tester"),
        pty=COLOR_OUTPUT,
    )
@task

def exec_test_suite_specific_requirement_china_tester(c):
    """execute testing with pip-requires.txt and demo tester"""
    c.run(
        make_cmd("exec-test-suite-specific-requirement-china-tester"),
        pty=COLOR_OUTPUT,
    )