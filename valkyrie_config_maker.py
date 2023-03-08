import random
from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
from typing import Generator, Generic, List, Type, TypeVar

from xoa_converter.converters.rfc2544.model import LegacyModel2544 as ValkyrieConfig2544
from xoa_converter.converters.rfc2889.model import ValkyrieConfiguration2889 as ValkyrieConfig2889


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