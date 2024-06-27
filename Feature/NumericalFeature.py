from .Feature import Feature

class NumericalFeature(Feature):

    def __init__(self):
        pass
    
    def nquantiles(data, removezeros=False):
        data_cp = data.copy()
        if removezeros is True and 0 in data_cp:
            data_cp.remove(0)
        length = len(data)
        if length < 9:
            raise Exception("dataset must have at least 9 values to calculate quantiles")
        data_cp = sorted(data_cp)
        quantiles = [0 for _ in range(0, 9)]

        for i in range(1, 10):
            pos = int(i * length / 10)
            quantiles[i - 1] = data_cp[pos]
        return quantiles
    
    def test_comb(data):
        return NumericalFeature.nquantiles(data, removezeros=False) + NumericalFeature.nquantiles(data, removezeros=True)
    
    def test_nat(data):
        return NumericalFeature.nquantiles(data, removezeros=False)
    
    def test_clr(data):
        return NumericalFeature.nquantiles(data, removezeros=True)