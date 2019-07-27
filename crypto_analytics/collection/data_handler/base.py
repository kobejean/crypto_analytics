import time
import pandas as pd
from abc import ABC, abstractmethod
from typing import Mapping, Optional

from crypto_analytics.collection.data_source import DataSource, TimeSeriesDataSource
from crypto_analytics.types import MergeType
from crypto_analytics.utils.typing import RealNumber, coalesce

class DataHandler(ABC):
    """ An abstract base class for all data handlers """
    DataSourcesType = Mapping[str, DataSource]

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


class ColumnMapper(DataHandler):
    """ A data handler base class that combines data sources and renames columns """
    ColumnMapType = Mapping[str, Mapping[str, str]]

    def __init__(self, data_sources: DataHandler.DataSourcesType,
                 column_map: ColumnMapType = {},
                 merge_type: MergeType = MergeType.INTERSECT):
        """ Creates the ColumnMapper data handler object """
        self.column_map = column_map
        self.merge_type = merge_type
        self.__to_time: Optional[RealNumber] = None
        super().__init__(data_sources)

    def fetch(self) -> pd.DataFrame:
        """ Fetches the data from all data sources and returns the data """
        merge_how = self.merge_type.to_merge_how()
        tmp_data = None

        # merge data sources
        for name, data_source in self.data_sources.items():
            # fetch data
            current_data = data_source.fetch()
            # rename columns
            columns = self.column_map.get(name, {})
            current_data.rename(columns=columns, inplace=True)
            current_data['time'] = data_source.get_time()
            # merge data
            if not tmp_data is None:
                tmp_data = pd.merge(tmp_data, current_data, how=merge_how,
                                    on='time', validate='one_to_one', sort=True)
            else:
                tmp_data = current_data

        self.data = tmp_data
        return self.data

    def write(self, filepath: str):
        """ Writes the currently stored data to a file """
        if self.data is None:
            raise Exception('No data to write')
        self.data.to_csv(filepath)

    def set_to_time(self, to_time: Optional[RealNumber]):
        for data_source in self.data_sources.values():
            if isinstance(data_source, TimeSeriesDataSource):
                data_source.set_to_time(to_time)
        self.__to_time = to_time

    def get_to_time(self) -> RealNumber:
        return coalesce(self.__to_time, lambda: time.time())
