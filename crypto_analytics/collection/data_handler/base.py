import pandas as pd
from abc import ABC, abstractmethod
from typing import Dict

from crypto_analytics.collection.data_source import DataSource

class DataHandler(ABC):
    DataSourcesType = Dict[str, DataSource]

    def __init__(self, data_sources: DataSourcesType):
        """ Creates the data handler object """
        self.data = None
        self.data_sources = data_sources
        super().__init__()

    @abstractmethod
    def fetch(self) -> pd.DataFrame:
        """ Fetches the data from all data sources and returns the data """
        pass

    @abstractmethod
    def write(self, filepath: str):
        """ Writes the currently stored data to a file """
        pass
