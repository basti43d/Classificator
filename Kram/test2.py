from Signatures.PatternSignature import PatternSignature
from Signatures.NumericalSignature import NumericalSignature
from Feature.RegexFeature import RegexFeature
from Feature.AggregateFeature import AggregateFeature
from Feature.NGramFeature import NGramFeature
from Classifiers.PatternClassificator import NaiveBayesClassificator
from Classifiers.QuantileClassificator import QuantileClassificator
from DataReader import DataReader
import csv

data = {
    "Vn": ["Franz", "Franziska"],
    "Str": ["Römerstraße", "Kaiserstraße"],
    "Nn": ["Gab", "Gat"]
}

test = [NGramFeature(ng) for ng in NGramFeature.ngram_ascii_lowercase_generator(n=2, count=60)]
real1 = NGramFeature.read_features("./NGrams/Vorname2Gram.txt")
real2 = NGramFeature.read_features("./NGrams/Strasse2Gram.txt")

ft = test + real1 + real2
sig = PatternSignature(["Vorname", "Strasse"], features=ft)

dr = DataReader()
dr.collect_file_data("./Data/", {"Vorname": "Vornamen.txt", "Strasse": "Strasse.txt"})

sig.learn_signatures(dr)


fs = sig.get_feature_dist()
tr, rel = sig.calc_top_features(40)

res = [x.pattern for x in tr]

vn = open("./NGrams/Vorname2Gram.txt", encoding="utf-8").read().split("\n")
str = open("./NGrams/Strasse2Gram.txt", encoding="utf-8").read().split("\n")

intersect = [x for x in res if x in vn or x in str]
#print(intersect)
out = [x for x in res if x not in intersect]
#print(out)

avn = [x for x in vn if x not in res]
astr = [x for x in str if x not in res]
#print(avn)
#print(astr)

vn_data = open("./Data/Vornamen.txt", encoding="utf-8").read().split("\n")
vn_ngr = NGramFeature.get_counted_ngrams(vn_data, n=2)

str_data = open("./Data/Strasse.txt", encoding="utf-8").read().split("\n")
str_ngr = NGramFeature.get_counted_ngrams(str_data, n=2)

s = "m "
#print(str_ngr[s])
#print(vn_ngr[s])