import pandas as pd
from abc import ABC, abstractmethod
from typing import Dict

from ..data_source import DataSource

class DataHandler(ABC):
    DataSourcesType = Dict[str, DataSource]

    def __init__(self, data_sources: DataSourcesType):
        self.data = None
        self.data_sources = data_sources
        super().__init__()

    @abstractmethod
    def fetch(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def write(self, filepath: str):
        pass
