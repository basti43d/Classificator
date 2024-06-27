from .Feature import Feature
import re

class RegexFeature(Feature):

    def __init__(self, pattern):
        if not isinstance(pattern, list):
            pattern = [pattern]
        self.pattern = pattern

    def test(self, data_entry):
        for pt in self.pattern:
            if re.search(pt, data_entry) is not None:
                return True
        return False
    
    def to_json(self):
        return {"type": "REGEX", "patterns": self.pattern}
    
    def read_features(path, combine: bool = False):
        features = open(path, encoding="utf-8").read().split("\n")
        if combine is True:
            return RegexFeature([ft for ft in features])
        return [RegexFeature(ft) for ft in features]