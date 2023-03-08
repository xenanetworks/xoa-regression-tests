from __future__ import annotations
import random
import asyncio
import json
from xoa_core import (
    controller,
    types,
)
from pathlib import Path
from xoa_converter.entry import converter
from xoa_converter.types import TestSuiteType

from valkyrie_config_maker import ValkyrieConfigMaker2889


BASE_PATH = Path(__file__).parent
TEST_ERROR_PATH = Path().resolve() / 'test_error'

def random_float(min: float, max: float, ndigits: int = 2) -> float:
    return round(random.uniform(min, max), ndigits=ndigits)


async def do_test():
    ctrl = await controller.MainController()

    print(ctrl.register_lib( str(BASE_PATH/'plugins') ))

    t197 = types.Credentials(
        product=types.EProductType.VALKYRIE,
        host="192.168.1.197"
    )
    t198 = types.Credentials(
        product=types.EProductType.VALKYRIE,
        host="192.168.1.198"
    )
    await ctrl.add_tester(t197)
    await ctrl.add_tester(t198)

    info = ctrl.get_test_suite_info("RFC-2889")
    if not info:
        print("Test suite is not recognized.")
        return None

    testing_config_maker = ValkyrieConfigMaker2889()
    testing_config_maker.add_base_config('test_config/6_port_throughput.v2889', 'test_config/4_port_throughput.v2889')
    for valkyrie_config in testing_config_maker.generate_testing_config():
        xoa_config = converter(TestSuiteType.RFC2889, valkyrie_config.json())
        xoa_config = json.loads(xoa_config)
        execution_id = ctrl.start_test_suite('RFC-2889', xoa_config)
        async for msg in ctrl.listen_changes(execution_id, _filter={types.EMsgType.STATISTICS}):
            if not isinstance(msg, dict):
                continue
            error_id = msg.payload.get('error_id')
            if error_id:
                with open(TEST_ERROR_PATH / str(error_id) / 'config.json', 'w') as fp:
                    xoa_config.dump(fp)


if __name__ == "__main__":
    asyncio.run(do_test())