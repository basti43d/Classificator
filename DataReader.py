import random

class DataReader:

    def __init__(self, data_dict=None):
        if data_dict is not None:
            self.attributes = list(data_dict.keys())
            self.attr_data = {}
            for attr in self.attributes:
                self.attr_data[attr] = data_dict[attr]
        else:
            self.attributes = []
            self.attr_data = {}
    
    def collect_file_data(self, path, attribute_files):
        self.attributes = list(attribute_files.keys())
        for attr in self.attributes:
            if not isinstance(attribute_files[attr], list):
                lst = [attribute_files[attr]]
            else:
                lst = attribute_files[attr]
            for file in lst:
                data = open(path + file, "r", encoding="utf-8").read()
                if attr not in self.attr_data:
                    self.attr_data[attr] = data.split("\n")
                else:
                    self.attr_data[attr] += data.split("\n")
    
    def get_attributes(self):
        return self.attributes
    
    def get_data(self, attr: str, samples: int = None, shuffle: bool = False) -> list[str]:
        if samples is not None and samples < len(self.attr_data[attr]):
            if shuffle is True:
                return random.sample(self.attr_data[attr], samples)
            else:
                return self.attr_data[attr][:samples]
        return self.attr_data[attr]

    def __split(self, data, number_of_chunks, shuffle=True):
        if shuffle is True:
            random.shuffle(data)
        entrys_per_chunk = int(len(data) / number_of_chunks)
        chunks = []
        first = 0
        last = entrys_per_chunk
        for i in range(0, number_of_chunks):
            if i == number_of_chunks - 1:
                last = len(data)
            chunks.append(data[first:last])
            first = last
            last += entrys_per_chunk
        return chunks
    
    def split_attr(self, attribute, number_of_chunks, shuffle=True):
        attr_chunks = self.__split(self.attr_data[attribute], number_of_chunks, shuffle)
        return [DataReader({attribute: attr_chunks[i]}) for i in range(number_of_chunks)]

    
    def split_all(self, number_of_chunks, shuffle=True):
        attr_chunks = [self.__split(self.attr_data[attr], number_of_chunks, shuffle) \
                        for attr in self.attributes]
        return [DataReader({self.attributes[i]: attr_chunks[i][j]  \
                    for i in range(len(self.attributes))}) \
                for j in range(number_of_chunks)]
    
    
    def check_numerical(data, accepted_rel_occ=0, ignore=['$', '%', '€'], accepted_perc=0, accepted_num=0):
        non_numerical_entrys = 0
        for entry in data:
            cleared = ''.join([c for c in str(entry) if c not in ignore])
            if cleared.isnumeric() is False:
                digits = sum(c.isdigit() for c in entry)
                if 1 - digits / len(entry) < accepted_rel_occ:
                    non_numerical_entrys += 1
        if accepted_perc > 0:
            accepted_num = accepted_perc * int(len(data))
        if non_numerical_entrys > accepted_num:
            return False
        return True
    

    def digit_filter(data):
        for i in range(0, len(data)):
            if not isinstance(data[i], str):
                raise Exception("can only convert strings")
            cleared = ''.join([c for c in data[i] if c.isdigit() or c in ['.', ',', 'e']])
            try:
                if '.' in cleared or ',' in cleared:
                    data[i] = float(cleared)
                else:
                    data[i] = int(cleared)
            except:
                continue
        return data
                