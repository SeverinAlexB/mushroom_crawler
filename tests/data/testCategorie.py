import unittest
from mushroom.data.Categorie import Categorie



class testCategorie(unittest.TestCase):
    def test_read_samples(self):
        path = "testdataset/cat3/"
        cat = Categorie.from_default(path, [1])
        cat.read_samples()
        self.assertEquals(len(cat.samples),15)