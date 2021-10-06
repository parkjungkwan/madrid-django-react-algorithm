from abc import abstractmethod, ABCMeta
from dataclasses import dataclass
from icecream import ic
import pandas as pd


@dataclass
class DFrameGenerator(object):

    train: object
    test: object
    id: str
    label: str
    fname: str

    @property
    def fname(self) -> object: return self._fname

    @fname.setter
    def fname(self, fname): self._fname = fname

    @property
    def train(self) -> object: return self._train

    @train.setter
    def train(self, train): self._train = train

    @property
    def test(self) -> object: return self._test

    @test.setter
    def test(self, test): self._test = test

    @property
    def id(self) -> str: return self._id

    @id.setter
    def id(self, id): self._id = id

    @property
    def label(self) -> str: return self._label

    @label.setter
    def label(self, label): self._label = label

    def create_model(self):
        return pd.read_csv(self.fname)

    def model_info(self, model):
        ic(model.head(3))
        ic(model.tail(3))
        ic(model.info())
        ic(model.describe())

class ReaderBase(metaclass=ABCMeta):
    @abstractmethod
    def new_file(self):
        pass

    @abstractmethod
    def csv(self):
        pass

    @abstractmethod
    def xls(self):
        pass

class Reader(ReaderBase):
    pass
