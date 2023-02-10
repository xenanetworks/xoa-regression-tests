from sys import platform
from invoke import task


COLOR_OUTPUT = platform == 'linux'


@task
def git_china(c):
    """execute testing with git-requires.txt and china tester"""
    c.run("tox -e git-china-tester", pty=COLOR_OUTPUT)

@task
def git_demo(c):
    """execute testing with git-requires.txt and demo tester"""
    c.run("tox -e git-demo-tester", pty=COLOR_OUTPUT)

@task
def pip_china(c):
    """execute testing with pip-requires.txt and china tester"""
    c.run("tox -e pip-china-tester", pty=COLOR_OUTPUT)

@task
def pip_demo(c):
    """execute testing with pip-requires.txt and demo tester"""
    c.run("tox -e pip-demo-tester", pty=COLOR_OUTPUT)