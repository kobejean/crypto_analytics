import pandas as pd
from abc import ABC, abstractmethod

class DataSource(ABC):
    def __init__(self):
        self.df = None
        super().__init__()

    @abstractmethod
    def fetch(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def write(self, filepath: str):
        pass
