from dataclasses import dataclass
from icecream import ic
import pandas as pd

@dataclass
class DFrameGenerator(object):

    train: object
    test: object
    id: str
    label: str
    dframe: object

    @property
    def dframe(self) -> object: return self._dframe

    @dframe.setter
    def dframe(self, fname): self._dframe = pd.read_csv(fname)

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

    def dframe_info(self):
        ic(self.dframe.head(3))
        ic(self.dframe.tail(3))
        ic(self.dframe.info())
        ic(self.dframe.describe())



