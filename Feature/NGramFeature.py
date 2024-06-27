from nltk import ngrams
from math import inf
import random
from DataReader import DataReader
from .Feature import Feature

class NGramFeature(Feature):

    def __init__(self, pattern):
        self.pattern = pattern

    def test(self, data_entry):
        if self.pattern in data_entry:
            return True
        return False
    
    def read_features(path: str) -> list:
        ngr =  open(path, encoding="utf-8").read().split("\n")
        return [NGramFeature(ng) for ng in ngr]

    def to_json(self) -> dict:
        return {"type": "NGRAM", "ngram": self.pattern}
    
    def get_ngrams(data: list[str], n: int = 2) -> list[str]:
        ng = [ngrams(data[i], n) for i in range(0, len(data))]
        return list(set([g for nng in ng for g in nng]))
    
    def get_counted_ngrams(data: list[str], n: int = 2, relative: bool = False) -> dict[str, int]:
        counted = {}
        for dt in data:
            for ng in ngrams(dt, n):
                ng = ''.join(ng)
                counted[ng] = counted.get(ng, 0) + 1
        if relative is True:
            for ng in counted.keys():
                counted[ng] /= len(data)
        return counted
    
    def extract_top_ngrams(data_reader: DataReader, n: int, count: int) -> list:
        rels, ngr = NGramFeature.calc_top_ngrams(data_reader, n)
        return [NGramFeature(ngr[i]) for i in range(count)]
        
    def calc_top_ngrams(data_reader: DataReader, n: int = 2, limit: int = None, k: int = 100):
        attributes = data_reader.get_attributes()
        attr_count = len(attributes)
        if attr_count <= 1:
            raise Exception("need at least 2 attributes to calculate most valuable features")
        pairs = [(attributes[i], attributes[j]) for i in range(attr_count) 
                                                for j in range(i + 1, attr_count)]
        ngrams = {attr: NGramFeature.get_counted_ngrams(data_reader.get_data(attr), n, relative=True) for attr in attributes}
        for attr in attributes:
            ngr = {k: v for k, v in sorted(ngrams[attr].items(), key=lambda item: item[1], reverse=True)}
            ngrams[attr] = dict(list(ngr.items())[:k])
        aggr = {}
        for attr in attributes:
            for ngr in ngrams[attr]:
                if ngr not in aggr:
                    aggr[ngr] = [1 - abs(max(ngrams[attr_i].get(ngr, 0), 1e-3) - max(ngrams[attr_j].get(ngr, 0), 1e-3)) for attr_i, attr_j in pairs]
                        
        limit = len(aggr.keys()) if limit is None else limit
        top_ngrams = []
        rels = [1.0 for _ in pairs] 
        for _ in range(limit):
            idx = rels.index(max(rels))
            mn = 2.0
            mft = None
            for ngr in aggr.keys():
                if aggr[ngr][idx] < mn:
                    mn = aggr[ngr][idx]
                    mft = ngr
            if mft is not None:
                top_ngrams.append(mft)
                for i, val in enumerate(aggr[mft]):
                    rels[i] *= val
                del aggr[mft]
        return rels, top_ngrams


    def attribute_relations(ngrams: list[str], signatures: dict[str, (list[int], list[int])]) -> list[(str, str), float]:
        attributes = list(signatures.keys())
        feature_count = len(signatures[attributes[0]])
        attr_count = len(attributes)
        cnt = 0
        pairs = [None for _ in range(0, int(attr_count * (attr_count - 1) / 2))]
        for i in range(0, attr_count):
            for j in range(i + 1, attr_count):
                tmp = 1.0
                x = [signatures[attributes[i]][0][k] / signatures[attributes[i]][1][k] for k in range(feature_count)]
                y = [signatures[attributes[j]][0][k] / signatures[attributes[j]][1][k] for k in range(feature_count)]
                for k in range(0, feature_count):
                    tmp *= max(min(x[k], y[k]), 1e-1)/max(x[k], y[k], 1e-1)
                pairs[cnt] = ((attributes[i], attributes[j]), tmp)
                cnt += 1
        return pairs
    
