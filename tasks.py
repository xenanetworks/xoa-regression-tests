from sys import platform
from invoke import task


COLOR_OUTPUT = platform == 'linux'


def make_cmd(env: str) -> str:
    return f"tox -e {env} -r"

@task
def git_china(c):
    """execute testing with git-requires.txt and china tester"""
    c.run(
        make_cmd("git-china-tester"),
        pty=COLOR_OUTPUT,
    )

@task
def git_demo(c):
    """execute testing with git-requires.txt and demo tester"""
    c.run(
        make_cmd("git-demo-tester"),
        pty=COLOR_OUTPUT,
    )

@task
def pip_china(c):
    """execute testing with pip-requires.txt and china tester"""
    c.run(
        make_cmd("pip-china-tester"),
        pty=COLOR_OUTPUT,
    )

@task
def pip_demo(c):
    """execute testing with pip-requires.txt and demo tester"""
    c.run(
        make_cmd("pip-demo-tester"),
        pty=COLOR_OUTPUT,
    )