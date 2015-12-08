from PIL import Image
import numpy as np
class Sample:
    def __init__(self):
        self.filepath = None
        self.tag = None
        self.numpy_array = None

    @classmethod
    def from_file(cls, path, tag):
        sample = cls()
        sample.filepath = path
        sample.tag = tag

        return sample

    def load_data(self):
        img = self._load_image(self.filepath)
        self.numpy_array = self._to_numpy_array_normalized(img)

    def _load_image(self, filepath):
        img = Image.open(self.filepath)
        img.load()
        img = img.convert('RGB')
        return img

    def _to_numpy_array_normalized(self, img):
        img_size = 224
        np_arr = np.asarray(img, dtype="int32")
        np_arr = np_arr.reshape(3, img_size, img_size)
        np_arr = np_arr.astype("float32")
        np_arr /= 255
        return np_arr