from .api import API
from .time import Time
from .Datasets import Datasets


datasets = Datasets(API)
__all__ = ["Time", "API", "datasets"]
__version__ = '2.1'
