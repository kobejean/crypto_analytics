import heapq, time, traceback
from datetime import datetime
from typing import Mapping, List, Tuple, Optional

from crypto_analytics.data_source import DataSource, OHLCDataSource
from crypto_analytics.controller import Controller
from crypto_analytics.types import Interval, MergeType, SymbolPair
from crypto_analytics.utils.typing import RealNumber
from crypto_analytics import utils

class ClosePriceController(Controller):
    """ A controller to convert currencies """

    def __init__(self, data_source: OHLCDataSource):
        """ Creates the CollectionController collection object """
        self._data_source = data_source

    def run(self):

        try:
            self._data_source.validated_fetch()
        except Exception:
            message = 'Failed to fetch data:\n{}'.format(traceback.format_exc())
            utils.console.error(message)

        return self._data_source.close.iloc[-1]
