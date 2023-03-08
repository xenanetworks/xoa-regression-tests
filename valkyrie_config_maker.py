import random
from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
from typing import Generator, Generic, List, Type, TypeVar

from xoa_converter.converters.rfc2544.model import LegacyModel2544 as ValkyrieConfig2544
from xoa_converter.converters.rfc2889.model import ValkyrieConfiguration2889 as ValkyrieConfig2889

from xoa_converter.converters.rfc2889.model import LegacyPortRateCapUnit


from xoa_converter.converters.rfc2889.model import (
    LegacyFecMode,
    LegacyPortRateCapProfile,
    LegacyPortRateCapUnit,
    LegacyTrafficDirection,
    LegacyTidAllocationScope,
    LegacyStreamRateType,
    BRRModeStr,
    LatencyMode,
)


class PortSpeedStr(Enum):
    AUTO = "auto"
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

T = TypeVar('T', ValkyrieConfig2889, ValkyrieConfig2544)

class ValkyrieConfigMakerBase(Generic[T], ABC):
    def __init__(self, valkyrie_config_class) -> None:
        self.base_configs_path: List[Path] = []
        self.valkyrie_config_class: T = valkyrie_config_class

    def add_base_config(self, *config_file_path: str) -> None:
        for path in config_file_path:
            self.base_configs_path.append(Path(path))

    def get_available_base_config_models(self) -> Generator[T, None, None]:
        for config_path in self.base_configs_path:
            yield self.valkyrie_config_class.parse_raw(config_path.read_text())

    @abstractmethod
    def generate_testing_config(self) -> Generator[Type[T], None, None]:
        raise NotImplementedError

    def iterate_enum_values(self, config_enum: Type[Enum]):
        return (i.value for i in config_enum)

    def random_float(self, min: float, max: float, ndigits: int = 2) -> float:
        return round(random.uniform(min, max), ndigits=ndigits)


GeneratorValkyrie2889 = Generator[ValkyrieConfig2889, None, None]

class ValkyrieConfigMaker2889(ValkyrieConfigMakerBase[ValkyrieConfig2889]):
    def __init__(self) -> None:
        super().__init__(ValkyrieConfig2889)

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
        for valkyrie_model, value in self.iterate_enum_values(PortSpeedStr):
            for port in valkyrie_model.port_handler.entity_list:
                port.port_speed = value
            yield valkyrie_model

    def e_LegacyTrafficDirection(self, valkyrie_model: ValkyrieConfig2889) -> GeneratorValkyrie2889:
        for valkyrie_model, value in self.iterate_enum_values(LegacyTrafficDirection):
            for test in valkyrie_model.test_options.test_type_option_map.rate_test.rate_sub_test_handler.rate_sub_tests:
                test.direction = value
            yield valkyrie_model

    def e_LegacyTidAllocationScope(self, valkyrie_model: ValkyrieConfig2889) -> GeneratorValkyrie2889:
        for valkyrie_model, value in self.iterate_enum_values(LegacyTidAllocationScope):
            valkyrie_model.tid_allocation_scope = value
            yield valkyrie_model

    def e_LegacyStreamRateType(self, valkyrie_model: ValkyrieConfig2889) -> GeneratorValkyrie2889:
        valkyrie_model.test_options.rate_definition.rate_type = LegacyStreamRateType.FRACTION
        valkyrie_model.test_options.rate_definition.rate_fraction = self.random_float(50, 99)
        yield valkyrie_model
        valkyrie_model = valkyrie_model.copy(deep=True)
        valkyrie_model.test_options.rate_definition.rate_type = LegacyStreamRateType.PPS
        valkyrie_model.test_options.rate_definition.rate_pps = self.random_float(50, 99)
        yield valkyrie_model
        for valkyrie_model, value in self.iterate_enum_values(LegacyPortRateCapUnit):
            valkyrie_model.test_options.rate_definition.rate_type = LegacyStreamRateType.L1BPS
            valkyrie_model.test_options.rate_definition.rate_bps_l1_unit = value
            valkyrie_model.test_options.rate_definition.rate_bps_l1 = self.random_float(50, 99)
            yield valkyrie_model
        for valkyrie_model, value in self.iterate_enum_values(LegacyPortRateCapUnit):
            valkyrie_model.test_options.rate_definition.rate_type = LegacyStreamRateType.L2BPS
            valkyrie_model.test_options.rate_definition.rate_bps_l2_unit = value
            valkyrie_model.test_options.rate_definition.rate_bps_l2 = self.random_float(50, 99)
            yield valkyrie_model

    def e_BRRMode(self, valkyrie_model: ValkyrieConfig2889) -> GeneratorValkyrie2889:
        for valkyrie_model, value in self.iterate_enum_values(BRRModeStr):
            for port in valkyrie_model.port_handler.entity_list:
                port.brr_mode = value
            yield valkyrie_model

    def e_LatencyMode(self, valkyrie_model: ValkyrieConfig2889) -> GeneratorValkyrie2889:
        for valkyrie_model, value in self.iterate_enum_values(LatencyMode):
            valkyrie_model.test_options.latency_mode = value
            yield valkyrie_model

    def e_MdiMdixMode(self, valkyrie_model: ValkyrieConfig2889) -> GeneratorValkyrie2889:
        for value in ('AUTO', 'MDI', 'MDIX'):
            for port in valkyrie_model.port_handler.entity_list:
                port.mdi_mdix_mode = value
            yield valkyrie_model

    def iter_change_enums(self, config: ValkyrieConfig2889) -> GeneratorValkyrie2889:
        for iteration_func in (
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
            for enum_changed_config in iteration_func(config):
                yield enum_changed_config

    def generate_testing_config(self) -> GeneratorValkyrie2889:
        for base_config in self.get_available_base_config_models():
            yield base_config # test all config without change anything

            # just test throughout with different enum value
            base_config.test_options.test_type_option_map.rate_test.enabled = False
            base_config.test_options.test_type_option_map.forward_pressure.enabled = False
            for enum_changed_config in self.iter_change_enums(base_config):
                yield enum_changed_config

