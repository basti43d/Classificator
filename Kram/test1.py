from Signatures.PatternSignature import PatternSignature
from Signatures.NumericalSignature import NumericalSignature
from Feature.RegexFeature import RegexFeature
from Feature.AggregateFeature import AggregateFeature
from Feature.NGramFeature import NGramFeature
from Classifiers.PatternClassificator import NaiveBayesClassificator
from Classifiers.QuantileClassificator import QuantileClassificator
from DataReader import DataReader

data_text = {
    "Vorname": "Vornamen.txt",
    "Nachname": "Nachnamen.txt",
    "Strasse": "Strasse.txt",
    "Stadt": "Stadt.txt",
    "Ort": "Ort.txt" 
}

data_num = {
    "Preis": "Preis.txt",
    "Plz": "Postleitzahl.txt",
    "Hausnummer": "Hausnummer.txt",
    "Zeit": "Zeit.txt",
    "Datum": "Datum.txt"
}

rf = RegexFeature.read_features("./Regexes/Strasse.txt")
nf = NGramFeature.read_features("./NGrams/Strasse2Gram.txt") + NGramFeature.read_features("./NGrams/Vorname2Gram.txt")

dr_num = DataReader()
dr_num.collect_file_data("./Data/", data_num)

dr = DataReader()
dr.collect_file_data("./Data/", data_text)

dr_learn, dr_test = dr.split_all(2)

ft = PatternSignature.use_features("./Features3.json")
sig = PatternSignature(["Vorname", "Strasse"], features=rf + nf)

sig.learn_signature("Vorname", dr_learn.attr_data["Vorname"])
sig.learn_signature("Strasse", dr_test.attr_data["Strasse"])

sig.write_signatures_top_features("./Features3.json", 50)

nbc = NaiveBayesClassificator(sig)

#print(nbc.attribute_confidence("Vorname", dr_test.attr_data["Vorname"], 100))
#print(nbc.attribute_confidence("Vorname", dr_test.attr_data["Strasse"], 100))
#print(nbc.attribute_confidence("Vorname", dr_num.attr_data["Hausnummer"], 100))

ns = NumericalSignature(NumericalSignature.test_nat)
ns.learn_signatures(dr_num)

print(ns.signature)

