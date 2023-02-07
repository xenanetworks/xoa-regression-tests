import json
import shutil
import pytest
import git
from dataclasses import dataclass
from pathlib import Path
from xoa_core import (
    controller,
    types,
)
from xoa_converter.entry import converter
from xoa_converter.types import TestSuiteType


# raise event loop error when test ended is normal !!
# https://github.com/pytest-dev/pytest-asyncio/issues/435


TS_GIT_REPO = 'https://github.com/xenanetworks/open-automation-test-suites'
TS_GIT_BRANCH = 'fix-use-enum-name'
TS_WILL_BE_TEST = (
    'plugin2544',
    'plugin2889',
)


TESTERS = (
    types.Credentials(
        product=types.EProductType.VALKYRIE,
        host="192.168.1.198"
    ),
    types.Credentials(
        product=types.EProductType.VALKYRIE,
        host="192.168.1.197"
    )
)


@dataclass
class TestSuiteInfo:
    suite_type: TestSuiteType
    valkyrie_config_path: str


VALKYRIE_CONFIG_FILE_2889 = 'test.v2889'
VALKYRIE_CONFIG_FILE_2544 = 'test.v2544'
suite_for_testing = (
    TestSuiteInfo(suite_type=TestSuiteType.RFC2544, valkyrie_config_path=VALKYRIE_CONFIG_FILE_2544),
    TestSuiteInfo(suite_type=TestSuiteType.RFC2889, valkyrie_config_path=VALKYRIE_CONFIG_FILE_2889),
)

def copy_ts_content(path_ts_git: Path, path_plugins: Path):
    for ts in TS_WILL_BE_TEST:
        shutil.move(str(path_ts_git / ts), str(path_plugins))


@pytest.fixture(scope="session")
def plugin_folder(tmp_path_factory):
    path_ts_git = tmp_path_factory.mktemp('ts')
    git.Repo.clone_from(TS_GIT_REPO, path_ts_git, branch=TS_GIT_BRANCH)
    path_plugins = tmp_path_factory.mktemp('plugins')
    copy_ts_content(path_ts_git, path_plugins)
    return path_plugins


@pytest.mark.asyncio
async def test_plugins(plugin_folder):
    xoa_controller = await controller.MainController()
    xoa_controller.register_lib( str(plugin_folder) )
    for tester in TESTERS:
        await xoa_controller.add_tester(tester)

    for test_suite in suite_for_testing:
        info = xoa_controller.get_test_suite_info(test_suite.suite_type.value)
        assert info
        with open(test_suite.valkyrie_config_path, "r") as f:
            new_data = converter(test_suite.suite_type, f.read())
            new_config = json.loads(new_data)
            execution_id = xoa_controller.start_test_suite(test_suite.suite_type.value, new_config)
            async for msg in xoa_controller.listen_changes(execution_id, _filter={types.EMsgType.STATISTICS}):
                assert msg