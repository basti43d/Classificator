from Signatures.PatternSignature import PatternSignature
from Signatures.NumericalSignature import NumericalSignature
from Feature.RegexFeature import RegexFeature
from Feature.AggregateFeature import AggregateFeature
from Feature.NGramFeature import NGramFeature
from Classifiers.PatternClassificator import PatternClassificator
from Classifiers.QuantileClassificator import QuantileClassificator
from DataReader import DataReader
import random

data = {
    "Vn": ["Franz", "Franziska"],
    "Str": ["Römerstraße", "Kaiserstraße"],
    "Nn": ["Gab", "Gat"]
}

data = open("./Vorname.txt")
s = ''
for d in data.read().splitlines():
    d = d.split(',')[0]
    s += d + '\n'
t = open('out.txt', 'w')
t.write(s)
t.close()








