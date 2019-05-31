import pandas as pd
from typing import Dict

from .base import DataHandler
from ..data_source import DataSource
from ...types import Interval, MergeType

class ColumnMapper(DataHandler):
    """ A data handler that combines data sources and renames columns """
    DataSourcesType = Dict[str, DataSource]
    ColumnMapType = Dict[str, Dict[str, str]]

    def __init__(self, data_sources: DataSourcesType,
                 column_map: ColumnMapType = {},
                 merge_type: MergeType = MergeType.INTERSECT):
        """ Creates the ColumnMapper data handler object """
        self.column_map = column_map
        self.merge_type = merge_type
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
                                    on='time', validate="one_to_one", sort=True)
            else:
                tmp_data = current_data

        self.data = tmp_data
        return self.data


    def write(self, filepath: str):
        """ Writes the currently stored data to a file """
        self.data.to_csv(filepath)
