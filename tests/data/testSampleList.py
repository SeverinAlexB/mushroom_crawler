import unittest
from mushroom.data.SampleList import SampleList
import numpy as np


class testSampleList(unittest.TestCase):
    def test_from_folder(self):
        slist = SampleList.from_folder("testdataset/cat1/", [1])
        self.assertEquals(len(slist), 2)
        sample = slist[0]
        self.assertEquals(sample.tag, [1])

    def test_load_data(self):
        slist = SampleList.from_folder("testdataset/cat1/", [1])
        slist.load_data()
        sample = slist[0]
        self.assertIsNotNone(sample.numpy_array)

    def test_toinput_response(self):
        slist = SampleList.from_folder("testdataset/cat1/", [1])
        slist.load_data()

        (x, y) = slist.to_input_response()
        self.assertEquals(len(x), 2)
        self.assertEquals(len(y), 2)
        self.assertTrue(np.array_equal(x[0], slist[0].numpy_array))

    def test_split(self):
        slist = SampleList.from_folder("testdataset/cat1/", [1])
        (train,test) = slist.split(0.5)
        self.assertEquals(len(train), 1)
        self.assertEquals(len(test), 1)
        self.assertEquals(train[0], slist[0])
        self.assertEquals(test[0], slist[1])



