from abc import abstractmethod
from DataReader import DataReader

class Signature:

    @abstractmethod
    def learn_signatures(data_reader: DataReader):
        pass