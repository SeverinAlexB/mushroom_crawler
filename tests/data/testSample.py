import unittest
from mushroom.data.Sample import Sample

class testSample(unittest.TestCase):
    def test_ctor(self):
        sample_path = "testdataset/cat1/Aleuria aurantia1.jpg"
        sample = Sample.from_file(sample_path, [1])
        sample.load_image()
        self.assertIsNotNone(sample.numpy_array)
        self.assertEquals(sample.filepath, sample_path)
        self.assertEquals(sample.tag, [1])