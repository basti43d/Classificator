
from abc import ABCMeta, abstractmethod
from Signatures import Signature


class Classificator():

    def __init__(self, signature: Signature):
        self.signature = signature
    
    @abstractmethod
    def classify(self, data):
        pass

    @abstractmethod
    def classification_probabilities(self, data):
        pass