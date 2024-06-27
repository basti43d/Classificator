import string
from .Feature import Feature

class AggregateFeature(Feature):

    def __init__(self, pattern):
        if not isinstance(pattern, list):
            pattern = [pattern]
        self.pattern = pattern
    
    def test(self, data_entry):
        for chr in self.pattern:
            if chr in data_entry:
                return True
        return False
    
    def read_features(path):
        lines = open(path, encoding="utf-8").read().split("\n")
        return [line.split(",").strip() for line in lines]

    
    def to_json(self):
        return {"type": "AGGREAGATE", "aggr": self.pattern}
    
    def create_letter_features():
        return AggregateFeature.create_lowercase_ascii_letter_features() + AggregateFeature.create_uppercase_ascii_letter_features()
    
    def create_lowercase_letter_features():
        return [AggregateFeature(pattern=c) for c in string.ascii_lowercase] + [AggregateFeature(pattern=c) for c in ["ä", "ö", "ü", "ß"]]
    
    def create_uppercase_letter_features():
        return [AggregateFeature(pattern=c) for c in string.ascii_uppercase] + [AggregateFeature(pattern=c) for c in ["Ä", "Ö", "Ü"]]
    
    def create_digit_features():
        return [AggregateFeature(pattern=c) for c in string.digits]
        
    def create_ascii_features():
        ar = []
        ar += [AggregateFeature(pattern=c) for c in string.ascii_letters]
        ar += [AggregateFeature(pattern=c) for c in string.digits]
        ar += [AggregateFeature(pattern=c) for c in ["\(", "\)", "\*", "\+", "\?", "\[", "\]", "\\\\", "\."]]
        ar += [AggregateFeature(pattern=c) for c in ["!", "@", "#", "$", "%"]]
        return ar
    
    def create_aggregate_features():
        features = []
        features.append(AggregateFeature(pattern=[c for c in string.ascii_letters]))
        features.append(AggregateFeature(pattern=[c for c in string.ascii_lowercase]))
        features.append(AggregateFeature(pattern=[c for c in string.ascii_uppercase]))
        features.append(AggregateFeature(pattern=["a", "e", "i", "o", "u"]))
        features.append(AggregateFeature(pattern=["A", "E", "I", "O", "U"]))
        features.append(AggregateFeature(pattern=[c for c in string.digits]))
        features.append(AggregateFeature(pattern=[c for c in string.ascii_letters] + [c for c in string.digits]))
        return features 