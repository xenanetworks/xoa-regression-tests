import asyncio
import os
import json
import shutil
import pytest
import git
import pytest_asyncio
from typing import Tuple
from pathlib import Path
from async_timeout import timeout

from xoa_core import (
    controller,
    types,
)
from xoa_converter.entry import converter
from xoa_converter.types import TestSuiteType


# raise event loop error when test ended is normal !!
# https://github.com/pytest-dev/pytest-asyncio/issues/435


TS_GIT_REPO = 'https://github.com/xenanetworks/open-automation-test-suites'
TS_GIT_BRANCH = os.getenv('TEST_SUITES_BRANCH') or 'dev'
WILL_TEST_TS_FOLDER_TAIL = (
    '2544',
    '2889',
    '3918',
)

TESTER_CHINA = (
    types.Credentials(
        product=types.EProductType.VALKYRIE,
        host="192.168.1.198"
    ),
    types.Credentials(
        product=types.EProductType.VALKYRIE,
        host="192.168.1.197"
    ),
)
TESTER_DEMO = (
    types.Credentials(
        product=types.EProductType.VALKYRIE,
        host="demo.xenanetworks.com"
    ),
)

def get_testers() -> Tuple[types.Credentials, ...]:
    tester = os.getenv('TESTERS')
    if tester == 'china':
        return TESTER_CHINA
    elif tester == 'demo':
        return TESTER_DEMO
    else:
        raise ValueError("Unknown tester")

def get_valkyire_config_path(_type: TestSuiteType) -> str:
    tester = os.getenv('TESTERS')
    assert tester in ('china', 'demo')
    file_extension = {
        TestSuiteType.RFC2544: 'v2544',
        TestSuiteType.RFC2889: 'v2889',
        TestSuiteType.RFC3918: 'v3918',
    }[_type]
    return f"{tester}.{file_extension}"

def copy_ts_folder_content(path_ts_git: Path, path_plugins: Path):
    for ts in WILL_TEST_TS_FOLDER_TAIL:
        shutil.move(str(path_ts_git / f"plugin{ts}"), str(path_plugins))

def with_timeout(t):
    def wrapper(corofunc):
        async def run(*args, **kwargs):
            try:
                with timeout(t):
                    return await corofunc(*args, **kwargs)
            except Exception as e:
                pytest.fail(str(e))
        return run
    return wrapper

@pytest.fixture(scope="session")
def plugin_folder(tmp_path_factory):
    path_git_ts_source = tmp_path_factory.mktemp('ts')
    git.Repo.clone_from(TS_GIT_REPO, path_git_ts_source, branch=TS_GIT_BRANCH)
    path_local_plugins = tmp_path_factory.mktemp('plugins')
    copy_ts_folder_content(path_git_ts_source, path_local_plugins)
    return path_local_plugins

@pytest.fixture(autouse=True)
def remove_core_store_file():
    if os.path.isfile('store'):
        os.remove('store')

# driver v1 incompatible with older version xena server
# dont know how to catch nested coroutine exception so adding timeout here
# https://github.com/pytest-dev/pytest-asyncio/issues/32
@pytest.mark.order(1)
@pytest.mark.asyncio
@with_timeout(15)
async def test_fast_fail():
    xoa_controller = await controller.MainController()
    for tester in get_testers():
        await xoa_controller.add_tester(tester)

@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()

@pytest_asyncio.fixture(scope="session")
async def xoa_controller(plugin_folder):
    ctrl = await controller.MainController()
    ctrl.register_lib( str(plugin_folder) )
    for tester in get_testers():
        await ctrl.add_tester(tester)
    return ctrl

async def start_ts(xoa_controller, test_suite):
    info = xoa_controller.get_test_suite_info(test_suite.value)
    assert info
    with open(get_valkyire_config_path(test_suite), "r") as f:
        new_data = converter(test_suite, f.read())
        new_config = json.loads(new_data)
        execution_id = xoa_controller.start_test_suite(test_suite.value, new_config)
        async for msg in xoa_controller.listen_changes(execution_id, _filter={types.EMsgType.STATISTICS}):
            assert msg

@pytest.mark.asyncio
async def test_2544(xoa_controller):
    await start_ts(xoa_controller, TestSuiteType.RFC2544)

@pytest.mark.asyncio
async def test_2889(xoa_controller):
    await start_ts(xoa_controller, TestSuiteType.RFC2889)

@pytest.mark.asyncio
async def test_3918(xoa_controller):
    await start_ts(xoa_controller, TestSuiteType.RFC3918)
