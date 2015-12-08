import glob
from Sample import Sample
import numpy as np
class SampleList(list):
    @classmethod
    def from_folder(cls, folder_path, tag):
        slist = cls()
        files = glob.glob(folder_path + "*.*")
        for file in files:
            sample = Sample.from_file(file, tag)
            slist.append(sample)
        return slist

    @classmethod
    def from_list(cls, samples):
        slist = cls()
        for s in samples:
            slist.append(s)
        return slist


    def load_data(self):
        for sample in self:
            sample.load_data()

    def to_input_response(self):
        if self[0].numpy_array is None:
            raise Exception("Load data first")

        inputs = []
        responses = []
        for sample in self:
            inputs.append(sample.numpy_array)
            responses.append(sample.tag)

        return (np.asarray(inputs), np.asarray(responses))

    def split(self, factor):
        split_point = int(len(self) * factor)
        train = self[0:split_point]
        test = self[split_point:len(self)]

        return (SampleList.from_list(train), SampleList.from_list(test) )

