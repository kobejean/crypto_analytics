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

    def __init__(self, pair: SymbolPair, data_sources: DataSourcesType):
        """ Creates the CollectionController collection object """
        queue = [(ds.to_time, name) for name, ds in data_sources.items()]
        heapq.heapify(queue)

        self.data_sources = data_sources
        self.queue = queue

    def run(self):
        while len(self.queue) > 0:
            # pop queue task
            fetch_time, data_source_name = heapq.heappop(self.queue)
            data_source = self.data_sources[data_source_name]

            # find time remaining and wait
            print(_format_queue(self.queue))
            print('Time remaining until fetch {0}:'.format(data_source_name))
            _countdown(fetch_time)

            # fetch data
            data_source.fetch()

            try:
                # validate data
                data_source.validate()
                # write to file
                start_time = data_source.time[0]
                start_date = datetime.utcfromtimestamp(start_time).strftime('%Y_%m_%d')
                filename = '{0}_{1}.csv'.format(data_source_name, start_date)
                data_source.write(filename)
            except Exception as e:
                print(e)

            # schedule and push new task to queue
            fetch_period = data_source.interval.to_unix_time() * data_source.rows
            next_fetch_time = fetch_time + fetch_period
            data_source.to_time = next_fetch_time
            heapq.heappush(self.queue, (next_fetch_time, data_source_name))

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
    string = 'Queue: ['
    for fetch_time, name in queue:
        time_formated = datetime.utcfromtimestamp(fetch_time).strftime('%m/%d/%Y, %H:%M:%S')
        string += '\n(time: "' + time_formated + '" data_source: "' + name + '"),'
    return string + '\n]'
