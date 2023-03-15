from typing import Generator, Generic, List, Type, TypeVar

from xoa_converter.converters.rfc2544.model import LegacyModel2544 as ValkyrieConfig2544
from valkyrie_config_maker import ValkyrieConfigMakerBase
from xoa_converter.converters.rfc2544 import enums
from plugins.plugin2544.utils import constants as const


T = TypeVar("T", ValkyrieConfig2544, ValkyrieConfig2544)


GeneratorValkyrie2544 = Generator[ValkyrieConfig2544, None, None]


class ValkyrieConfigMaker2544(ValkyrieConfigMakerBase[ValkyrieConfig2544]):
    def __init__(self) -> None:
        super().__init__(ValkyrieConfig2544)

    # PortConfiguration
    def e_LegacyFecMode(
        self, valkyrie_model: ValkyrieConfig2544
    ) -> GeneratorValkyrie2544:
        for e in self.iterate_enum(enums.LegacyFecMode):
            for port in valkyrie_model.port_handler.entity_list:
                port.fec_mode = e
            yield valkyrie_model

    def e_LegacyPortRateCapUnit(
        self, valkyrie_model: ValkyrieConfig2544
    ) -> GeneratorValkyrie2544:
        for e in self.iterate_enum(enums.LegacyPortRateCapUnit):
            for port in valkyrie_model.port_handler.entity_list:
                port.port_rate_cap_profile = (
                    enums.LegacyPortRateCapProfile.CUSTOM_RATE_CAP
                )
                port.port_rate_cap_unit = e
                port.enable_port_rate_cap = True
            yield valkyrie_model

    def e_PortSpeed(self, valkyrie_model: ValkyrieConfig2544) -> GeneratorValkyrie2544:
        for value in self.iterate_enum(const.PortSpeedStr):
            for port in valkyrie_model.port_handler.entity_list:
                port.port_speed = value.value
            yield valkyrie_model

    def e_BRRMode(self, valkyrie_model: ValkyrieConfig2544) -> GeneratorValkyrie2544:
        for value in self.iterate_enum(const.BRRModeStr):
            for port in valkyrie_model.port_handler.entity_list:
                port.brr_mode = value.value
            yield valkyrie_model

    def e_MdiMdixMode(
        self, valkyrie_model: ValkyrieConfig2544
    ) -> GeneratorValkyrie2544:
        for e in self.iterate_enum(const.MdiMdixMode):
            for port in valkyrie_model.port_handler.entity_list:
                port.mdi_mdix_mode = e.value
            yield valkyrie_model

    def e_AutoNegotiation(
        self, valkyrie_model: ValkyrieConfig2544
    ) -> GeneratorValkyrie2544:
        for port in valkyrie_model.port_handler.entity_list:
            port.auto_neg_enabled = not port.auto_neg_enabled
        yield valkyrie_model

    def e_ANLT(self, valkyrie_model: ValkyrieConfig2544) -> GeneratorValkyrie2544:
        for port in valkyrie_model.port_handler.entity_list:
            port.auto_neg_enabled = not port.anlt_enabled
        yield valkyrie_model

    # TestConfiguration - Topology and Frame Content
    # 1. Overall Test Topology
    def e_LegacyTrafficDirection(
        self, valkyrie_model: ValkyrieConfig2544
    ) -> GeneratorValkyrie2544:
        for e in self.iterate_enum(enums.LegacyTrafficDirection):
            valkyrie_model.test_options.topology_config.direction = e
            yield valkyrie_model

    # 2. Frame Sizes
    def e_LegacyPacketSizeType(
        self, valkyrie_model: ValkyrieConfig2544
    ) -> GeneratorValkyrie2544:
        for e in self.iterate_enum(enums.LegacyPacketSizeType):
            valkyrie_model.test_options.packet_sizes.packet_size_type = e
            yield valkyrie_model

    # 3. Frame Test Payload
    def e_UseMicroTPLD(
        self, valkyrie_model: ValkyrieConfig2544
    ) -> GeneratorValkyrie2544:
        flag = (
            valkyrie_model.test_options.flow_creation_options.use_micro_tpld_on_demand
        )
        flag = not flag
        yield valkyrie_model

    def e_PayloadType(
        self, valkyrie_model: ValkyrieConfig2544
    ) -> GeneratorValkyrie2544:
        for e in self.iterate_enum(const.PayloadTypeStr):
            valkyrie_model.test_options.payload_definition.payload_type = e.value
            yield valkyrie_model

    # TestConfiguration - Test Excetion Control
    # 1. Flow Creation
    def e_LegacyFlowCreationType(
        self, valkyrie_model: ValkyrieConfig2544
    ) -> GeneratorValkyrie2544:
        for e in self.iterate_enum(enums.LegacyFlowCreationType):
            valkyrie_model.test_options.flow_creation_options.flow_creation_type = e

            yield valkyrie_model

    def e_LegacyTidAllocationScope(
        self, valkyrie_model: ValkyrieConfig2544
    ) -> GeneratorValkyrie2544:
        t = valkyrie_model.test_options.flow_creation_options.flow_creation_type
        for e in self.iterate_enum(enums.LegacyTidAllocationScope):
            if t == enums.LegacyFlowCreationType.STREAM_BASED:
                continue
            valkyrie_model.test_options.flow_creation_options.flow_creation_type = (
                enums.LegacyFlowCreationType.STREAM_BASED
            )
            valkyrie_model.tid_allocation_scope = e
            yield valkyrie_model

    # 2. Port Scheduling
    def e_SpeedReductSweep(
        self, valkyrie_model: ValkyrieConfig2544
    ) -> GeneratorValkyrie2544:
        flag = valkyrie_model.test_options.enable_speed_reduct_sweep
        flag = not flag
        yield valkyrie_model

    def e_UsePortSyncStart(
        self, valkyrie_model: ValkyrieConfig2544
    ) -> GeneratorValkyrie2544:
        flag = valkyrie_model.test_options.use_port_sync_start
        flag = not flag
        yield valkyrie_model

    # 3. Test Scheduling
    def e_LegacyOuterLoopMode(
        self, valkyrie_model: ValkyrieConfig2544
    ) -> GeneratorValkyrie2544:
        for e in self.iterate_enum(enums.LegacyOuterLoopMode):
            valkyrie_model.test_options.outer_loop_mode = e
            yield valkyrie_model

    # 4. MAC Learning Options
    def e_LegacyMACLearningMode(
        self, valkyrie_model: ValkyrieConfig2544
    ) -> GeneratorValkyrie2544:
        for e in self.iterate_enum(enums.LegacyMACLearningMode):
            valkyrie_model.test_options.learning_options.mac_learning_mode = e
            yield valkyrie_model

    def e_TogglePortSync(
        self, valkyrie_model: ValkyrieConfig2544
    ) -> GeneratorValkyrie2544:
        flag = valkyrie_model.test_options.toggle_sync_state
        flag = not flag
        yield valkyrie_model

    # 5. ARP/NDP Learning Options
    def e_EnableRefresh(
        self, valkyrie_model: ValkyrieConfig2544
    ) -> GeneratorValkyrie2544:
        flag = valkyrie_model.test_options.learning_options.arp_refresh_enabled
        flag = not flag
        yield valkyrie_model

    def e_GWMACasDMAC(
        self, valkyrie_model: ValkyrieConfig2544
    ) -> GeneratorValkyrie2544:
        # TODO: require L3
        flag = valkyrie_model.test_options.flow_creation_options.use_gateway_mac_as_dmac
        flag = not flag
        yield valkyrie_model

    # 6. Flow-Based Learning Option
    def e_FlowBasedLearningPreamble(
        self, valkyrie_model: ValkyrieConfig2544
    ) -> GeneratorValkyrie2544:
        flag = (
            valkyrie_model.test_options.learning_options.use_flow_based_learning_preamble
        )
        flag = not flag
        yield valkyrie_model

    # 7. Reset and Error Handling
    def e_ResetandErrorHandling(
        self, valkyrie_model: ValkyrieConfig2544
    ) -> GeneratorValkyrie2544:
        # valkyrie_model.test_options.should_stop_on_los = False
        flag = valkyrie_model.test_options.should_stop_on_los
        flag = not flag
        yield valkyrie_model

    # TestTypeConfiguration - Throughput
    # 1. Rate Iteration Options
    def e_LegacySearchType(
        self, valkyrie_model: ValkyrieConfig2544
    ) -> GeneratorValkyrie2544:
        valkyrie_model.test_options.test_type_option_map.throughput.enabled = True
        valkyrie_model.test_options.test_type_option_map.latency.enabled = False
        valkyrie_model.test_options.test_type_option_map.loss.enabled = False
        valkyrie_model.test_options.test_type_option_map.back2_back.enabled = False
        for e in self.iterate_enum(enums.LegacySearchType):
            valkyrie_model.test_options.test_type_option_map.throughput.rate_iteration_options.search_type = (
                e
            )
            yield valkyrie_model

    def e_LegacyRateResultScopeType(
        self, valkyrie_model: ValkyrieConfig2544
    ) -> GeneratorValkyrie2544:
        valkyrie_model.test_options.test_type_option_map.throughput.enabled = True
        valkyrie_model.test_options.test_type_option_map.latency.enabled = False
        valkyrie_model.test_options.test_type_option_map.loss.enabled = False
        valkyrie_model.test_options.test_type_option_map.back2_back.enabled = False
        for e in self.iterate_enum(enums.LegacyRateResultScopeType):
            valkyrie_model.test_options.test_type_option_map.throughput.rate_iteration_options.result_scope =                 e
            
            yield valkyrie_model

    # Pass Criteria
    def e_UsePassThreshold(
        self, valkyrie_model: ValkyrieConfig2544
    ) -> GeneratorValkyrie2544:
        valkyrie_model.test_options.test_type_option_map.throughput.enabled = True
        valkyrie_model.test_options.test_type_option_map.latency.enabled = False
        valkyrie_model.test_options.test_type_option_map.loss.enabled = False
        valkyrie_model.test_options.test_type_option_map.back2_back.enabled = False
        flag = (
            valkyrie_model.test_options.test_type_option_map.throughput.rate_iteration_options.use_pass_threshold
        )
        flag = not flag
        yield valkyrie_model

    # TestTypeConfiguration - Latency
    def e_LatencyModeStr(
        self, valkyrie_model: ValkyrieConfig2544
    ) -> GeneratorValkyrie2544:
        valkyrie_model.test_options.test_type_option_map.throughput.enabled = False
        valkyrie_model.test_options.test_type_option_map.latency.enabled = True
        valkyrie_model.test_options.test_type_option_map.loss.enabled = False
        valkyrie_model.test_options.test_type_option_map.back2_back.enabled = False
        for e in self.iterate_enum(const.LatencyModeStr):
            valkyrie_model.test_options.test_type_option_map.latency.latency_mode = (
                e.value
            )
            yield valkyrie_model

    def e_RelativeToThroughput(
        self, valkyrie_model: ValkyrieConfig2544
    ) -> GeneratorValkyrie2544:
        valkyrie_model.test_options.test_type_option_map.throughput.enabled = True
        valkyrie_model.test_options.test_type_option_map.latency.enabled = True
        valkyrie_model.test_options.test_type_option_map.loss.enabled = False
        valkyrie_model.test_options.test_type_option_map.back2_back.enabled = False
        flag = (
            valkyrie_model.test_options.test_type_option_map.latency.rate_relative_tput_max_rate
        )
        flag = not flag
        yield valkyrie_model

        valkyrie_model.test_options.test_type_option_map.throughput.enabled = False
        valkyrie_model.test_options.test_type_option_map.latency.rate_relative_tput_max_rate = (
            True
        )
        yield valkyrie_model

    # TestTypeConfiguration - FrameLoss
    def e_UsePassCriteria(
        self, valkyrie_model: ValkyrieConfig2544
    ) -> GeneratorValkyrie2544:
        valkyrie_model.test_options.test_type_option_map.throughput.enabled = False
        valkyrie_model.test_options.test_type_option_map.latency.enabled = False
        valkyrie_model.test_options.test_type_option_map.loss.enabled = True
        valkyrie_model.test_options.test_type_option_map.back2_back.enabled = False
        flag = (
            valkyrie_model.test_options.test_type_option_map.throughput.rate_iteration_options.use_pass_threshold
        )
        flag = not flag
        yield valkyrie_model

    def e_GapMonitorEnable(
        self, valkyrie_model: ValkyrieConfig2544
    ) -> GeneratorValkyrie2544:
        valkyrie_model.test_options.test_type_option_map.throughput.enabled = False
        valkyrie_model.test_options.test_type_option_map.latency.enabled = False
        valkyrie_model.test_options.test_type_option_map.loss.enabled = True
        valkyrie_model.test_options.test_type_option_map.back2_back.enabled = False
        flag = (
            valkyrie_model.test_options.test_type_option_map.throughput.rate_iteration_options.use_pass_threshold
        )
        flag = not flag
        yield valkyrie_model

    def iter_change_enums(self, config: ValkyrieConfig2544) -> GeneratorValkyrie2544:
        for iteration_func in (
            # TestConfiguration
            self.e_LegacyTrafficDirection,
            self.e_LegacyPacketSizeType,
            self.e_UseMicroTPLD,
            self.e_PayloadType,
            self.e_LegacyFlowCreationType,
            self.e_LegacyTidAllocationScope,
            self.e_SpeedReductSweep,
            self.e_UsePortSyncStart,
            self.e_LegacyOuterLoopMode,
            self.e_LegacyMACLearningMode,
            self.e_TogglePortSync,
            self.e_EnableRefresh,
            self.e_GWMACasDMAC,
            self.e_FlowBasedLearningPreamble,
            self.e_ResetandErrorHandling,
            # Port Configuration
            self.e_LegacyFecMode,
            self.e_LegacyPortRateCapUnit,
            self.e_PortSpeed,
            self.e_BRRMode,
            self.e_MdiMdixMode,
            # TestTypeConfiguration
            self.e_LegacySearchType,
            self.e_LegacyRateResultScopeType,
            self.e_UsePassThreshold,
            self.e_LatencyModeStr,
            self.e_RelativeToThroughput,
            self.e_UsePassCriteria,
            self.e_GapMonitorEnable,
        ):
            for enum_changed_config in iteration_func(config.copy(deep=True)):
                yield enum_changed_config

    def generate_testing_config(self) -> GeneratorValkyrie2544:
        for base_config in self.get_available_base_config_models():
            yield base_config.copy(deep=True)  # test all config without change anything
            for enum_changed_config in self.iter_change_enums(
                base_config.copy(deep=True)
            ):
                yield enum_changed_config
