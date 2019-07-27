import heapq, time
import pandas as pd
from datetime import datetime

from crypto_analytics.controller import Controller
from crypto_analytics.types import Interval, MergeType
from crypto_analytics.types.symbol import SymbolPair
from typing import Mapping, List, Tuple, Optional

from crypto_analytics.collection.data_source import DataSource, TimeSeriesDataSource
from crypto_analytics.utils.typing import RealNumber

class CollectionController(Controller):
    """ A controller to collect data from data sources """
    DataSourcesType = Mapping[str, TimeSeriesDataSource]
    QueueItem = Tuple[RealNumber, str]

    def __init__(self, pair: SymbolPair, data_sources: DataSourcesType):
        """ Creates the CollectionController collection object """
        queue = [(ds.get_to_time(), name) for name, ds in data_sources.items()]
        heapq.heapify(queue)

        self.data_sources = data_sources
        self.queue = queue

    def run(self):
        while len(self.queue) > 0:
            fetch_time, data_source_name = heapq.heappop(self.queue)
            data_source = self.data_sources[data_source_name]
            time_remaining = max(fetch_time - time.time(), 0)
            print('Time remaining until fetch {0}: {1}s'.format(data_source_name, time_remaining))
            time.sleep(time_remaining)

            data_source.fetch()

            print(data_source.data)
            if isinstance(data_source.data, pd.DataFrame) and not data_source.data.empty:
                start_time = data_source.get_time()[0]
                start_date = datetime.utcfromtimestamp(start_time).strftime('%Y_%m_%d')
                filename = '{0}_{1}.csv'.format(data_source_name, start_date)
                data_source.write(filename)

                fetch_period = data_source.interval.to_unix_time() * data_source.rows
                next_fetch_time = fetch_time + fetch_period
                data_source.set_to_time(next_fetch_time)

                heapq.heappush(self.queue, (next_fetch_time, data_source_name))
