from .Classificator import Classificator
from Signatures.PatternSignature import PatternSignature
import random
import math

class PatternClassificator(Classificator):

    def __init__(self, signature: PatternSignature):
        super().__init__(signature)
    

    def classify(self, data: list[str], sample_size: int = None):
        expected_attr = None
        val = -1
        for attr in self.signature.attributes:
            prob = self.classify_attribute(attr, data, sample_size)
            if prob > val:
                val = prob
                expected_attr = attr
        return expected_attr

    def classify_attributes(self, data: list[str], sample_size: int = None):
        cp = {}
        for attr in self.signature.attributes:
            cp[attr] = self.classify_attribute(attribute=attr, data=data, sample_size=sample_size)
        return cp


    def classify_attribute(self, attribute: str, data: list[str], sample_size: int = None):
        if sample_size is not None and sample_size < len(data):
            data = PatternClassificator.__samples(data, sample_size=sample_size)
        features = self.signature.features
        if attribute not in self.signature.signature:
            raise Exception("attribute not in signature")
        attr_sig = self.signature.signature[attribute]
        data_sig = self.signature.learn_signature(attribute, data, forget=True)
        prob_data = 0.0
        prob_attr = 0.0

        data_sig_tested = data_sig[1]
        data_sig_matched = data_sig[0]

        for i in range(0, len(data_sig[0])):
            x = data_sig_matched[i] / data_sig_tested[i]
            if x != 0:
                prob_data += data_sig_matched[i] * math.log2(x)
            y = data_sig_tested[i] - data_sig_matched[i]
            x = y / data_sig_tested[i]
            if x != 0:
                prob_data += y * math.log2(x)

        for entry in data:
            for i, feature in enumerate(features):
                f = feature.test(entry)
                c = attr_sig[0][i]
                w = attr_sig[1][i]
                if f is True and c == 0 or f is False and w == c:
                    d = 1/2
                else:
                    d = f * c + (1 - f) * (w - c)
                prob_attr += math.log2(d)
        prob_attr -= len(data) * sum([math.log2(attr_sig[1][i]) for i in range(len(features))])
        
        if abs(prob_attr) < 1e-10:
            return 1
        if abs(prob_data) < 1e-10:
            prob_data = math.log2(1/2)
        return prob_data / prob_attr

    def __samples(data, sample_size):
        return random.sample(data, sample_size)