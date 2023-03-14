from __future__ import annotations
import random
import asyncio
import platform
import json
import time
import hashlib
import uuid
import os
import traceback
from pydantic import BaseModel
from xoa_core import (
    controller,
    types,
)
from pathlib import Path
from xoa_converter.converters.rfc2544.adapter import Converter2544
from xoa_converter.converters.rfc2544.model import LegacyModel2544
from xoa_core.core import const
from valkyrie_config_maker2544 import ValkyrieConfigMaker2544
from plugins.plugin2544.plugin.statistics import FinalStatistic

SAVED_CONFIG_PATH = Path().resolve() / "test_export"
RESULT_PATH = Path().resolve() / "test_result"


BASE_PATH = Path(__file__).parent
TEST_ERROR_PATH = Path().resolve() / "test_error"


def clear():
    path = Path().resolve()
    for file in os.listdir(path):
        file_name_sp = file.split(".")
        if file_name_sp[-1] == "log":  # remove log file
            abspath = os.path.join(path, file)
            os.remove(abspath)

    for file in os.listdir(SAVED_CONFIG_PATH):
        abspath = os.path.join(SAVED_CONFIG_PATH, file)
        os.remove(abspath)

    for file in os.listdir(RESULT_PATH):
        abspath = os.path.join(RESULT_PATH, file)
        os.remove(abspath)
    # for file in os.listdir(TEST_ERROR_PATH):
    #     abspath = os.path.join(TEST_ERROR_PATH, file)
    #     os.remove(abspath)


class Converter2544Testing(Converter2544):
    def __init__(self, model: LegacyModel2544):
        self.id_map = {}
        self.data = model.copy(deep=True)



def set_windows_loop_policy():
    plat = platform.system().lower()
    if plat == "windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def save_xoa_config(config: str, filename: str) -> None:
    with open(SAVED_CONFIG_PATH / f"{filename}.json", "w") as fp:
        fp.write(config)


async def do_test(ctrl: controller.MainController, file_paths: list):
    testing_config_maker = ValkyrieConfigMaker2544()
    testing_config_maker.add_base_config(*file_paths)
    is_exists = {}
    overlap = 0
    for valkyrie_config in testing_config_maker.generate_testing_config():
        filename = uuid.uuid4().hex
        xoa_config_dict = Converter2544Testing(valkyrie_config).gen()
        xoa_config_json = json.dumps(xoa_config_dict, indent=2, sort_keys=True)
        md5 = hashlib.md5(xoa_config_json.encode("utf-8")).hexdigest()
        if md5 in is_exists:
            overlap += 1
            continue
        is_exists[md5] = True
        save_xoa_config(xoa_config_json, filename)
        # continue
        try:
            execution_id = ctrl.start_test_suite("RFC-2544", xoa_config_dict)
            async for msg in ctrl.listen_changes(
                execution_id,
                const.PIPE_EXECUTOR,
                const.PIPE_RESOURCES,
                _filter={types.EMsgType.STATISTICS, types.EMsgType.ERROR},
            ):
                # with open(f"{RESULT_PATH}/{filename}.log", "a+") as fp:
                #     fp.write(type(msg.payload))
                if isinstance(msg.payload, BaseModel):
                    # if msg.payload.is_final:
                    #     print("")
                    with open(f"{RESULT_PATH}/{filename}.log", "a+") as fp:
                        fp.write(msg.payload.json(indent=2))
                elif isinstance(msg.payload, dict):
                    with open(f"{RESULT_PATH}/{filename}.log", "a+") as fp:
                        fp.write(json.dumps(msg.payload, indent=2))
                    error_id = msg.payload.get("error_id")
                    if error_id:
                        with open(
                            TEST_ERROR_PATH / str(error_id) / "config.json", "a+"
                        ) as fp:
                            json.dump(xoa_config_dict, fp, indent=2)
           

        except Exception:
            tb_exc = traceback.format_exc()
            error_id = hashlib.md5(tb_exc.encode("utf-8")).hexdigest()
            current_error_path = TEST_ERROR_PATH / error_id
            current_error_path.mkdir(exist_ok=True)
            with open(current_error_path / "traceback.txt", "w") as error_log:
                traceback.print_exc(file=error_log)


async def main():
    ctrl = await controller.MainController()

    print(ctrl.register_lib(str(BASE_PATH / "plugins")))

    t197 = types.Credentials(product=types.EProductType.VALKYRIE, host="192.168.1.197")
    t198 = types.Credentials(product=types.EProductType.VALKYRIE, host="192.168.1.198")
    await ctrl.add_tester(t197)
    await ctrl.add_tester(t198)

    info = ctrl.get_test_suite_info("RFC-2544")
    if not info:
        print("Test suite is not recognized.")
        return None

    with open("test_config/config.json", "r") as fp:
        config = json.load(fp)

    await asyncio.gather(*[do_test(ctrl, file_paths) for file_paths in config.values()])


if __name__ == "__main__":
    clear()
    set_windows_loop_policy()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    # asyncio.run_(main())
