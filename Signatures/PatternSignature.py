import json
from math import sqrt, inf
from enum import Enum
from Feature.Feature import Feature
from Feature.RegexFeature import RegexFeature
from Feature.NGramFeature import NGramFeature
from Feature.AggregateFeature import AggregateFeature
from DataReader import DataReader

class FeatureType(str, Enum):
    REGEX = "REGEX",
    NGRAM = "NGRAM",
    AGGREGATE = "AGGREGATE"

class PatternSignature:

    def __init__(self, attributes: list[str] = None, features: list[Feature] = None, signature_obj = None):
        if attributes is None and signature_obj is None:
            raise Exception("Attributes must be defined")
        if signature_obj is None and features is None:
            raise Exception("Features must be defined")
        self.attributes = []
        self.features = []
        self.signature = {}
        if signature_obj is not None:
            self.attributes = signature_obj["attributes"]
            self.features = signature_obj["features"]
            self.matched = signature_obj["matched"]
            self.signature = signature_obj["signature"]
            if features is not None:
                features = PatternSignature.remove_duplicate_features(features=features, ref=self.features)
                self.features += features
                for attr in self.attributes:
                    self.signature[attr][0] += [0 for _ in range(0, len(features))]
                    self.signature[attr][1] += [0 for _ in range(0, len(features))]
        else:
            self.features = PatternSignature.remove_duplicate_features(features=features)
            self.matched = [0 for _ in self.features]
        if attributes is not None:
            attributes = [attr for attr in attributes if attr not in self.attributes]
            self.attributes += attributes
            for attr in attributes:
                self.signature[attr] = ([0 for _ in self.features], [0 for _ in self.features])
    

    def learn_signature(self, attribute: str, data: list[str], overwrite: bool = False, forget: bool = False) -> None:
        if overwrite is True:
            self.__reset(attribute)
        if attribute not in self.attributes:
            raise Exception("attribute not defined in signature.")
        tmp = [0 for _ in range(0, len(self.features))]
        for i, feature in enumerate(self.features):
            for entry in data:
                if feature.test(entry) is True:
                    tmp[i] += 1
                    if forget is False:
                        self.matched[i] += 1
        if forget is True:
            return (tmp, [len(data) for _ in range(len(self.features))])
        for i in range(0, len(self.features)):
            self.signature[attribute][0][i] += tmp[i]
            self.signature[attribute][1][i] += len(data)
    

    def learn_signatures(self, data_reader: DataReader, overwrite: bool = False) -> None:
        for attr in data_reader.get_attributes():
            self.learn_signature(attr, data_reader.get_data(attr), overwrite)
    

    def replace_feature(self, feature_new, feature_old, new_signature : dict = None) -> None:
        if feature_old not in self.features:
            raise Exception("feature not in signatures feature set")
        idx = self.features.index(feature_old)
        self.features[idx] = feature_new
        if new_signature is not None:
            if len(list(new_signature.keys())) != len(list(self.signature.keys())):
                raise Exception("invalid attribute list")
            for attr in dict:
                if attr not in self.signature:
                    raise Exception("attribute " + attr + " does not exist in signature")
            self.signature[attr][0] = new_signature[attr][0]
            self.signature[attr][1] = new_signature[attr][1]

        
    def __reset(self, attribute: str) -> None:
        self.signature[attribute][0] = [0 for _ in self.features]
        self.signature[attribute][1] = [0 for _ in self.features]

    def use_features(path, alpha=0.9, use_signature: bool = True) -> dict:
        jstr = open(path, "r").read()
        js = json.loads(jstr)
        features = []
        matched = []
        for feature in js["features"]:
            if(feature["type"] == FeatureType.REGEX):
                features.append(RegexFeature(feature["patterns"]))
            elif(feature["type"] == FeatureType.NGRAM):
                features.append(NGramFeature(feature["ngram"]))
            elif(feature["type"] == FeatureType.AGGREGATE):
                features.append(AggregateFeature(feature["aggr"]))
            matched.append(feature["matched"])
        if use_signature is True:
            signatures = {}
            for attribute in js["attributes"]:
                signatures[attribute["attribute"]] = [attribute["matched"], attribute["tested"]]
        else:
            signatures = None
        ret =  {
            "attributes": list(signatures.keys()),
            "features": features,
            "matched": matched,
            "signature": signatures
        }
        return ret
    
    
    def get_feature_dist(self):
        attr_count = len(self.attributes)
        feature_sig = {}
        for i in range(len(self.features)):
            ft = self.features[i]
            feature_sig[ft] = {}
            fractures = []
            for j in range(attr_count):
                frac = self.get_signature_frac(self.attributes[j], i)
                fractures.append(frac)
                for k in range(0, j):
                    if frac == 0 and fractures[k] == 0:
                        tmp = 1.0
                    else:
                        tmp = max(min(frac, fractures[k]), 1) / max(frac, fractures[k])
                    feature_sig[ft][(self.attributes[k], self.attributes[j])] = tmp
        return feature_sig
    
    def calc_top_features(self, count: int = None):
        attr_count = len(self.attributes)
        if attr_count <= 1:
            raise Exception("need at least 2 attributes to calculate most valuable features")
        ft_count = len(self.features) if count is None else count
        top_features = []
        feature_sig = self.get_feature_dist()
        pairs = [(self.attributes[i], self.attributes[j]) for i in range(attr_count) 
                                                        for j in range(i + 1, attr_count)]
        rels = [1.0 for _ in range(int((attr_count - 1) * attr_count / 2))] 
        for _ in range(ft_count):
            idx = rels.index(max(rels))
            pair = pairs[idx]
            mn = inf
            mft = None
            for ft in feature_sig:
                if feature_sig[ft][pair] < mn:
                    mn = feature_sig[ft][pair]
                    mft = ft
            if mft is not None:
                top_features.append(mft)
                rels[idx] *= mn
                del feature_sig[mft]
        return top_features


    def get_signature_frac(self, attr, i):
        return self.signature[attr][0][i] / self.signature[attr][1][i]
        
    
    def write_signature(self, path, selected_features: list[Feature] = None) -> None:
        if selected_features is None: 
            selected_features = self.features
        features = [None for _ in selected_features]
        for i, feature in enumerate(selected_features):
            ft = feature.to_json()
            ft["matched"] = self.matched[self.features.index(feature)]
            features[i] = ft

        sig = {attr: ([self.signature[attr][0][self.features.index(ft)] for ft in selected_features], \
                      [self.signature[attr][1][self.features.index(ft)] for ft in selected_features]) \
                for attr in self.attributes}
        attributes = [{"attribute": attr, 
                       "matched": sig[attr][0],
                       "tested": sig[attr][1]} for attr in self.attributes]
        job = {"features": features, "attributes": attributes}

        jstr = json.dumps(job, indent=2)
        file = open(path, "w")
        file.write(jstr)
    
    def write_signature_top_features(self, path: str, feature_limit: int) -> None:
        top_features = [None for _ in range(0, len(self.features))] 
        for i in range(0, len(self.features)):
            score = [self.signature[attr][0][i] / max(self.signature[attr][1][i], 1) for attr in self.attributes]
            top_features[i] = (max(score) / max(sum(score), 1), self.features[i])
        top_features.sort(key=lambda x: x[0], reverse=True)
        top_features = [top_features[i][1] for i in range(0, feature_limit)]
        self.write_signatures(path, selected_features=top_features)
    
    
    def euklidian_distance(sig1, sig2):
        r = 0
        if len(sig1[0]) is not len(sig2[0]):
            raise Exception("vectors must be of same length")
        for i in range(0, len(sig1[0])):
            x = sig1[0][i] / sig1[1][i]
            y = sig2[0][i] / sig2[1][i]
            r += (x - y) * (x - y)
        return sqrt(r)
    
    def manhattan_distance(sig1, sig2):
        r = 0
        if len(sig1[0]) is not len(sig2[0]):
            raise Exception("vectors must be of same length")
        for i in range(0, len(sig1[0])):
            x = sig1[0][i] / sig1[1][i]
            y = sig2[0][i] / sig2[1][i]
            r += abs(x - y) + abs(x - y)
            return r
    
    def calculate_confusion_matrix(self, distance_func=euklidian_distance):
        length = len(self.attributes)
        matrix = [[0 for _ in range(0, length)] for _ in range(0, length)]
        for i in range(0, length):
            for j in range(i + 1, length):
                dist = distance_func(self.signature[self.attributes[i]], self.signature[self.attributes[j]])       
                matrix[i][j] = dist
                matrix[j][i] = dist
        return matrix

    def calculate_confusion_distances(self, distance_func=euklidian_distance):
        dist = {}
        min = inf
        for attr_i in self.attributes:
            for attr_j in self.attributes:
                if attr_i == attr_j:
                    continue
                tmp = distance_func(self.signature[attr_i], self.signature[attr_j])
                if tmp < min: 
                    min = tmp
            dist[attr_i] = min
        return dist


    def remove_duplicate_features(features: list[Feature], ref: list[Feature] = None) -> list[Feature]:
        ref = [] if ref is None else ref
        st = []
        for i in range(len(features)):
            b = True
            for f in ref:
                if f == features[i]:
                    b = False
                    break
            for j in range(i + 1, len(features)):
                if features[i] == features[j]:
                    b = False
                    break
            if b is True:
                st.append(features[i])
        return st