from abc import abstractmethod

class Feature:

    def __init__(self, pattern):
        self.pattern = pattern

    @abstractmethod
    def test(self, data_entry):
        pass

    @abstractmethod
    def read_features(self, path):
        pass
    
    def __eq__(self, other):
        if not isinstance(other, Feature):
            return False
        if not self.pattern == other.pattern:
            return False