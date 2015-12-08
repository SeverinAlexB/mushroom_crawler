import unittest
from mushroom.data.Dataset import Dataset

class testDataset(unittest.TestCase):
    def test_nb_categories(self):
        dataset = Dataset.from_sourcefolder("testdataset/")
        nb_categories = len(dataset.categories)
        self.assertEquals(nb_categories,3)

    def test_shuffled(self):
        dataset = Dataset.from_sourcefolder("testdataset/")
        dataset.read_samples()
        nb_samples = len(dataset.samples_shuffled)
        self.assertEquals(nb_samples, 19)

    def test_use(self):
        dataset = Dataset.from_sourcefolder("testdataset/")
        dataset.read_samples()
        (train,test) = dataset.samples_shuffled.split(0.6)
        self.assertEquals(len(train), 4)
        train.load_data()
        (x,y) = train.to_input_response()
        self.assertEquals(len(x), 4)


