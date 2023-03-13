from __future__ import annotations
from enum import Enum
import asyncio
import hashlib
import json
import time
from typing import Generator
import uuid
from xoa_core import (
    controller,
    types,
)
from pathlib import Path
from xoa_converter.converters.rfc2889.model import ValkyrieConfiguration2889 as ValkyrieConfig2889
from xoa_converter.converters.rfc2889.adapter import Converter2889Testing
from xoa_converter.entry import ComplexEncoder
from valkyrie_config_maker import ValkyrieConfigMakerBase
from xoa_converter.converters.rfc2889.model import (
    LegacyFecMode,
    LegacyPortRateCapProfile,
    LegacyPortRateCapUnit,
    LegacyTrafficDirection,
    LegacyTidAllocationScope,
    LegacyStreamRateType,
    BRRModeStr,
    LatencyMode,
    TestPortMacMode,
    LearningSequencePortDMacMode,
    LearningPortDMacMode,
    LegacyPacketSizeType,
)


class PortSpeedStr(Enum):
    AUTO = "AUTO"
    F100M = "f100m"
    F1G = "f1g"
    F2500M = "f2500m"
    F5G = "f5g"
    F10G = "f10g"
    F100M1G = "f100m1g"
    F100M1G2500M = "f100m1g2500m"
    F10M = "f10m"
    F40G = "f40g"
    F100G = "f100g"
    F10MHDX = "f10mhdx"
    F100MHDX = "f100mhdx"
    F10M100M = "f10m100m"
    F100M1G10G = "f100m1g10g"
    F25G = "f25g"
    F50G = "f50g"
    F200G = "f200g"
    F400G = "f400g"
    F800G = "f800g"
    F1600G = "f1600g"
    UNKNOWN = "unknown"

BASE_PATH = Path(__file__).parent
TEST_ERROR_PATH = Path().resolve() / 'test_error'
SAVED_CONFIG_PATH = Path().resolve() / 'saved_config'

GeneratorValkyrie2889 = Generator[ValkyrieConfig2889, None, None]

class ValkyrieConfigMaker2889(ValkyrieConfigMakerBase[ValkyrieConfig2889]):
    def __init__(self) -> None:
        super().__init__(ValkyrieConfig2889)
        self.test_types = (
            "rate_test",
            "congestion_control",
            "forward_pressure",
            "max_forwarding_rate",
            "address_caching_capacity",
            "address_learning_rate",
            "broadcast_forwarding",
        )

    def e_LegacyFecMode(self, valkyrie_model: ValkyrieConfig2889) -> GeneratorValkyrie2889:
        for value in self.iterate_enum_values(LegacyFecMode):
            for port in valkyrie_model.port_handler.entity_list:
                port.fec_mode = value
            yield valkyrie_model

    def e_LegacyPortRateCapUnit(self, valkyrie_model: ValkyrieConfig2889) -> GeneratorValkyrie2889:
        for value in self.iterate_enum_values(LegacyPortRateCapUnit):
            for port in valkyrie_model.port_handler.entity_list:
                port.port_rate_cap_profile = LegacyPortRateCapProfile.CUSTOM
                port.port_rate_cap_unit = value
                port.enable_port_rate_cap = True
            yield valkyrie_model

    def e_PortSpeed(self, valkyrie_model: ValkyrieConfig2889) -> GeneratorValkyrie2889:
        for value in self.iterate_enum_values(PortSpeedStr):
            for port in valkyrie_model.port_handler.entity_list:
                port.port_speed = value
            yield valkyrie_model

    def e_LegacyTrafficDirection(self, valkyrie_model: ValkyrieConfig2889) -> GeneratorValkyrie2889:
        for value in self.iterate_enum_values(LegacyTrafficDirection):
            for test in valkyrie_model.test_options.test_type_option_map.rate_test.rate_sub_test_handler.rate_sub_tests:
                test.direction = value
            yield valkyrie_model

    def e_LegacyTidAllocationScope(self, valkyrie_model: ValkyrieConfig2889) -> GeneratorValkyrie2889:
        for value in self.iterate_enum_values(LegacyTidAllocationScope):
            valkyrie_model.tid_allocation_scope = value
            yield valkyrie_model

    def e_LegacyStreamRateType(self, valkyrie_model: ValkyrieConfig2889) -> GeneratorValkyrie2889:
        valkyrie_model.test_options.rate_definition.rate_type = LegacyStreamRateType.FRACTION
        valkyrie_model.test_options.rate_definition.rate_fraction = self.random_float(50, 99)
        yield valkyrie_model
        valkyrie_model.test_options.rate_definition.rate_type = LegacyStreamRateType.PPS
        valkyrie_model.test_options.rate_definition.rate_pps = self.random_float(50, 99)
        yield valkyrie_model
        for value in self.iterate_enum_values(LegacyPortRateCapUnit):
            valkyrie_model.test_options.rate_definition.rate_type = LegacyStreamRateType.L1BPS
            valkyrie_model.test_options.rate_definition.rate_bps_l1_unit = value
            valkyrie_model.test_options.rate_definition.rate_bps_l1 = self.random_float(50, 99)
            yield valkyrie_model
        for value in self.iterate_enum_values(LegacyPortRateCapUnit):
            valkyrie_model.test_options.rate_definition.rate_type = LegacyStreamRateType.L2BPS
            valkyrie_model.test_options.rate_definition.rate_bps_l2_unit = value
            valkyrie_model.test_options.rate_definition.rate_bps_l2 = self.random_float(50, 99)
            yield valkyrie_model

    def e_BRRMode(self, valkyrie_model: ValkyrieConfig2889) -> GeneratorValkyrie2889:
        for value in self.iterate_enum_values(BRRModeStr):
            for port in valkyrie_model.port_handler.entity_list:
                port.brr_mode = value
            yield valkyrie_model

    def e_LatencyMode(self, valkyrie_model: ValkyrieConfig2889) -> GeneratorValkyrie2889:
        for value in self.iterate_enum_values(LatencyMode):
            valkyrie_model.test_options.latency_mode = value
            yield valkyrie_model

    def e_MdiMdixMode(self, valkyrie_model: ValkyrieConfig2889) -> GeneratorValkyrie2889:
        for value in ('AUTO', 'MDI', 'MDIX'):
            for port in valkyrie_model.port_handler.entity_list:
                port.mdi_mdix_mode = value
            yield valkyrie_model

    def e_TestPortMacMode(self, valkyrie_model: ValkyrieConfig2889) -> GeneratorValkyrie2889:
        for value in self.iterate_enum_values(TestPortMacMode):
            valkyrie_model.test_options.test_type_option_map.address_caching_capacity.test_port_mac_mode = value
            valkyrie_model.test_options.test_type_option_map.address_learning_rate.test_port_mac_mode = value
            yield valkyrie_model

    def e_LearningPortDMacMode(self, valkyrie_model: ValkyrieConfig2889) -> GeneratorValkyrie2889:
        for value in self.iterate_enum_values(LearningPortDMacMode):
            valkyrie_model.test_options.test_type_option_map.address_caching_capacity.learning_port_dmac_mode = value
            valkyrie_model.test_options.test_type_option_map.address_learning_rate.learning_port_dmac_mode = value
            yield valkyrie_model

    def e_LearningSequencePortDMacMode(self, valkyrie_model: ValkyrieConfig2889) -> GeneratorValkyrie2889:
        for value in self.iterate_enum_values(LearningSequencePortDMacMode):
            valkyrie_model.test_options.test_type_option_map.address_caching_capacity.learning_sequence_port_dmac_mode = value
            valkyrie_model.test_options.test_type_option_map.address_learning_rate.learning_sequence_port_dmac_mode = value
            yield valkyrie_model

    def e_LegacyPacketSizeType(self, valkyrie_model: ValkyrieConfig2889) -> GeneratorValkyrie2889:
        for value in self.iterate_enum_values(LegacyPacketSizeType):
            valkyrie_model.test_options.packet_sizes.packet_size_type = value
            yield valkyrie_model

    def iter_change_enums(self, config: ValkyrieConfig2889) -> GeneratorValkyrie2889:
        # just test throughout with different enum value
        self.toggle_all_test_type(config, False)
        config.test_options.test_type_option_map.rate_test.enabled = True
        for iteration_func in (
            self.e_LegacyPacketSizeType,
            self.e_LegacyFecMode,
            self.e_LegacyPortRateCapUnit,
            self.e_PortSpeed,
            self.e_LegacyTrafficDirection,
            self.e_LegacyTidAllocationScope,
            self.e_LegacyStreamRateType,
            self.e_BRRMode,
            self.e_LatencyMode,
            self.e_MdiMdixMode,
        ):
            print(iteration_func)
            for enum_changed_config in iteration_func(config):
                yield enum_changed_config


    def toggle_all_test_type(self, config: ValkyrieConfig2889, status: bool) -> None:
        for each_type in self.test_types:
            each_config = getattr(config.test_options.test_type_option_map, each_type)
            each_config.enabled = status

    def test_each_test_type_separately(self, config: ValkyrieConfig2889) -> GeneratorValkyrie2889:
        self.toggle_all_test_type(config, False)

        for each_type in self.test_types:
            each_config = getattr(config.test_options.test_type_option_map, each_type)
            each_config.enabled = True
            yield config
            each_config.enabled = False

    def test_address_learning(self, config: ValkyrieConfig2889) -> GeneratorValkyrie2889:
        self.toggle_all_test_type(config, False)
        config.test_options.test_type_option_map.address_caching_capacity.enabled = True
        config.test_options.test_type_option_map.address_learning_rate.enabled = True
        yield from self.e_TestPortMacMode(config)
        yield from self.e_LearningPortDMacMode(config)
        yield from self.e_LearningSequencePortDMacMode(config)

        config.test_options.test_type_option_map.address_caching_capacity.toggle_sync_state ^= True
        config.test_options.test_type_option_map.address_learning_rate.toggle_sync_state ^= True
        yield config
        config.test_options.test_type_option_map.address_caching_capacity.toggle_sync_state ^= True
        config.test_options.test_type_option_map.address_learning_rate.toggle_sync_state ^= True

        config.test_options.test_type_option_map.address_learning_rate.switch_test_port_roles ^= True
        config.test_options.test_type_option_map.address_caching_capacity.switch_test_port_roles ^= True
        yield config
        config.test_options.test_type_option_map.address_learning_rate.switch_test_port_roles ^= True
        config.test_options.test_type_option_map.address_caching_capacity.switch_test_port_roles ^= True

        config.test_options.test_type_option_map.address_learning_rate.only_use_capacity ^= True
        yield config
        config.test_options.test_type_option_map.address_learning_rate.only_use_capacity ^= True

        config.test_options.test_type_option_map.address_learning_rate.set_end_address_to_capacity ^= True
        yield config
        config.test_options.test_type_option_map.address_learning_rate.set_end_address_to_capacity ^= True

    def toggle_boolean_field(self, config: ValkyrieConfig2889) -> GeneratorValkyrie2889:
        config.test_options.toggle_sync_state ^= True
        yield config
        config.test_options.toggle_sync_state ^= True

        config.test_options.use_port_sync_start ^= True
        yield config
        config.test_options.use_port_sync_start ^= True

        config.test_options.flow_creation_options.use_micro_tpld_on_demand ^= True
        yield config
        config.test_options.flow_creation_options.use_micro_tpld_on_demand ^= True

        self.toggle_all_test_type(config, False)
        config.test_options.test_type_option_map.max_forwarding_rate.enabled = True
        config.test_options.test_type_option_map.max_forwarding_rate.use_throughput_as_start_value ^= True
        yield config
        config.test_options.test_type_option_map.max_forwarding_rate.enabled = False

        config.test_options.test_type_option_map.errored_frames_filtering.enabled = True
        config.test_options.test_type_option_map.errored_frames_filtering.oversize_test_enabled ^= False
        yield config

    def generate_testing_config(self) -> GeneratorValkyrie2889:

        for base_config in self.get_available_base_config_models():
            # new_config = base_config.copy(deep=True) # test each config without change anything
            # yield new_config
            # yield from self.toggle_boolean_field(base_config.copy(deep=True))
            # yield from self.test_each_test_type_separately(base_config.copy(deep=True))
            yield from self.iter_change_enums(base_config.copy(deep=True))
            yield from self.test_address_learning(base_config.copy(deep=True))


def save_xoa_config(config: str) -> None:
    with open(SAVED_CONFIG_PATH / f'{uuid.uuid4().hex}.json', 'w') as fp:
        fp.write(config)

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
    testing_config_maker.add_base_config('test_config/6_port_throughput.v2889')
    is_exists = {}
    overlap = 0
    executed_time = []
    for valkyrie_config in testing_config_maker.generate_testing_config():
        start = int(time.time())
        xoa_config = Converter2889Testing(valkyrie_config).gen()
        xoa_config = json.dumps(xoa_config, indent=2, cls=ComplexEncoder, sort_keys=True)
        md5 = hashlib.md5(xoa_config.encode('utf-8')).hexdigest()
        if md5 in is_exists:
            overlap += 1
            continue
        is_exists[md5] = True
        save_xoa_config(xoa_config)
        continue
        xoa_config = json.loads(xoa_config)
        execution_id = ctrl.start_test_suite('RFC-2889', xoa_config)
        async for msg in ctrl.listen_changes(execution_id, _filter={types.EMsgType.STATISTICS}):
            if not isinstance(msg.payload, dict):
                continue
            error_id = msg.payload.get('error_id')
            if error_id:
                with open(TEST_ERROR_PATH / str(error_id) / 'config.json', 'w') as fp:
                    json.dump(xoa_config, fp, indent=2)
        end = int(time.time())
        executed_time.append(end-start)
    print(overlap)
    print(executed_time)

if __name__ == "__main__":
    asyncio.run(do_test())