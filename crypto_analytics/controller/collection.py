import heapq, time
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

    def __init__(self, pair: SymbolPair, data_sources: DataSourcesType, redundancy: int = 1):
        """ Creates the CollectionController collection object """
        queue: List[Tuple[RealNumber, int, str]] = []
        for copy_id in range(redundancy):
            for name, data_source in data_sources.items():
                redundancy_spacing = copy_id * (data_source.fetch_period / redundancy)
                fetch_time = data_source.to_time + redundancy_spacing

                queue.append((fetch_time, copy_id, name))

        heapq.heapify(queue)

        self._redundancy = redundancy
        self._data_sources = data_sources
        self._queue = queue


    @property
    def redundancy(self) -> int:
        return self._redundancy

    @property
    def data_sources(self) -> DataSourcesType:
        return self._data_sources

    def run(self):
        while len(self._queue) > 0:
            print(_format_queue(self._queue))
            # pop queue task
            fetch_time, copy_id, source_name = heapq.heappop(self._queue)
            data_source = self.data_sources[source_name]

            # find time remaining and wait
            print('Time remaining until fetch {0}:'.format(source_name))
            _countdown(fetch_time)

            # fetch data
            data_source.to_time = fetch_time
            data_source.fetch()

            try:
                # validate data
                data_source.validate()
                # write to file
                start_time = data_source.time[0]
                start_date = datetime.utcfromtimestamp(start_time).strftime('%Y_%m_%d')
                filename = '{}_{}_{}.csv'.format(source_name, copy_id, start_date)
                data_source.write(filename)
            except Exception as e:
                print(e)

            # schedule and push new task to queue
            next_fetch_time = fetch_time + data_source.fetch_period
            heapq.heappush(self._queue, (next_fetch_time, copy_id, source_name))


# private helper functions

def _countdown(to_time):
    time_remaining = max(to_time - time.time(), 0)
    while time_remaining > 0:
        time_formated = _format_time_remaining(time_remaining)
        print('T:', time_formated, end='\r')
        time.sleep(1)
        time_remaining = max(to_time - time.time(), 0)
    print('Time reached')

def _format_time_remaining(time_remaining) -> str:
    hrs, rem_hr = divmod(time_remaining, 3600)
    mins, secs = divmod(rem_hr, 60)
    return '{:.0f}:{:02.0f}:{:02.0f}'.format(hrs, mins, secs)

def _format_queue(queue) -> str:
    string = 'Priority Queue: ['
    for fetch_time, copy_id, source_name in queue:
        time_formated = datetime.utcfromtimestamp(fetch_time).strftime('%m/%d/%Y, %H:%M:%S')
        string += '\ntime: "{}" copy_id: {} source_name: "{}"'.format(time_formated, copy_id, source_name)
    return string + '\n]'
