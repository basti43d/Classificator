import json

class NumericalSignature:

    def __init__(self, test_method):
        self.signature = {}
        self.test_method = test_method

    def learn_signature(self, attribute, data, forget=False):
        quantiles = self.test_method(data)
        if forget is True:
            return quantiles
        self.signature[attribute] = quantiles
    
    def learn_signatures(self, data_reader):
        self.attributes = list(data_reader.attr_data.keys())
        for attr, data in data_reader.attr_data.items():
            self.learn_signature(attr, data)
    
    def append_signature(self, attribute, data, alpha=0.5, beta=0.5):
        if not attribute in self.signature:
            raise Exception("no signature for given attribute")
        sig = self.learn_signature(attribute, data, forget=True)
        for i in range(0, 9):
            self.signature[attribute][i] = alpha * sig[i] + beta * self.signature[attribute][i]
    
    def append_signatures(self, data_reader, alpha=0.5, beta=0.5):
        for attr, data in data_reader.attr_data.items():
            self.append_signature(attr, data, alpha, beta)
    

    def nquantiles(data, removezeros=False):
        data_cp = data.copy()
        if removezeros is True and 0 in data_cp:
            data_cp.remove(0)
        length = len(data)
        if length < 9:
            raise Exception("dataset must have at least 10 values to calculate quantiles")
        inc = int(length / 10)
        quantiles = [0 for _ in range(0, 9)]
        data_cp = sorted(data_cp)
        pos = 0

        for i in range(0, 9):
            pos += inc
            quantiles[i] = data_cp[pos - 1]
        return quantiles
    
    def read_signatures(self, path):
        jstr = open(path, "r").read()
        job = json.loads(jstr)
        for attr in job:
            self.signature[attr["attribute"]] = attr["signature"]

    
    def write_signatures(self, path):
        job = [{"attribute": attr, "signature": self.signature[attr]} for attr in self.attributes]
        jstr = json.dumps(job, indent=2)
        f = open(path, "w")
        f.write(jstr)

    
    def test_comb(data):
        return NumericalSignature.nquantiles(data, removezeros=False) + \
               NumericalSignature.nquantiles(data, removezeros=True)
    
    def test_nat(data):
        return NumericalSignature.nquantiles(data, removezeros=False)
    
    def test_clr(data):
        return NumericalSignature.nquantiles(data, removezeros=True)