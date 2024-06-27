from .Classificator import Classificator
from math import inf

class QuantileClassificator(Classificator):
    
    def __init__(self, signature):
        super().__init__(signature) 

    def classify_vote(self, data):
        attributes = self.signature.attributes
        votes = [0 for _ in range(0, len(attributes))]
        tmp = [0 for _ in range(0, len(attributes))]
        quantiles = self.signature.test_method(data)
        for i in range(0, len(quantiles)):
            min = inf 
            for j, attr in enumerate(attributes):
                attr_quantile = self.signature.signature[attr][i]
                tmp[j] = abs(attr_quantile - quantiles[i])
                if tmp[j] < min:
                    min = tmp[j]
            
            inc = 1 / tmp.count(min)
            for j in range(0, len(tmp)):
                if tmp[j] == min:
                    votes[j] += inc
                tmp[j] = 0
        return self.signature.attributes[votes.index(max(votes))]
    

    def classify_sum(self, data):
        min = inf
        min_attr = None
        quantiles = self.signature.test_method(None, data)
        for attr in self.signature.attributes:
            attr_quantiles = self.signature.signature[attr]
            print(attr_quantiles)
            sig = 0
            for j in range(0, len(attr_quantiles)):
                sig += abs(quantiles[j] - attr_quantiles[j])
            if sig < min:
                min = sig
                min_attr = attr
        return min_attr
    

    def classify_rank(self, data):
        vote = [0 for _ in self.signature.attributes]
        quantiles = self.signature.test_method(None, data)

        for i, attr in enumerate(self.signature.attributes):
            attr_quantiles = self.signature.signature[attr]
            for j in range(1, len(quantiles)):
                vote[i] += abs((attr_quantiles[j] - quantiles[j]) / (attr_quantiles[j] - attr_quantiles[j - 1]))
        return self.signature.attributes[vote.index(min(vote))]
