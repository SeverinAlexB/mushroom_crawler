from PIL import Image
import numpy as np
import glob
from random import shuffle
import gc

class Dataset:
    def __init__(self):
        self.sourcefolder = None
        self.categorie_infos = []
        self.categories = {}
        self.samples_shuffled = None

    @classmethod
    def from_sourcefolder(cls, sourcefolder):
        set = cls()
        set.sourcefolder = sourcefolder
        return set

    @classmethod
    def from_samples(cls, samples):
        set = cls()
        set.samples_shuffled = samples
        return set

    def read_samples(self):
        for info in self.categorie_infos:
            samples = Categorie.from_default(self.sourcefolder + info.folder, info.tag)
            samples.read_folder()
            self.categories[info] = samples

        all_samples = []
        for info in self.categorie_infos:
            samples = self.categories[info].samples
            all_samples += samples

        self.samples_shuffled = all_samples
        shuffle(self.samples_shuffled)

    def load_images(self):
        for info in self.categorie_infos:
            self.categories[info].load_samples()

    def split_train_test(self, train_factor):
        nb_samples = len(self.samples_shuffled)
        split_id = int(nb_samples * train_factor)

        train_samples = self.samples_shuffled[0:split_id]
        test_samples = self.samples_shuffled[split_id:nb_samples]

        train_set = Dataset.from_samples(train_samples)
        test_set = Dataset.from_samples(test_samples)
        return (train_set, test_set)

    def to_input_response(self):
        inputs = []
        responses = []
        for sample in self.samples_shuffled:
            sample.load_image()
            inputs.append(sample.numpy_array)
            responses.append(sample.tag)

        return (np.asarray(inputs), np.asarray(responses))



class CategorieInfo:
    def __init__(self):
        self.folder = ""
        self.tag = []

    @classmethod
    def from_default(cls, folder, tag):
        info = cls()
        info.folder = folder
        info.tag = tag
        return info



class Categorie:
    def __init__(self):
        self.sourcefolder = ""
        self.tag = None
        self.samples = []

    @classmethod
    def from_default(cls, sourcefolder, tag):
        categorie = cls()
        categorie.sourcefolder = sourcefolder
        categorie.tag = tag
        return categorie

    def read_folder(self):
        self.samples = []
        files = glob.glob(self.sourcefolder + "*.*")
        for file in files[:20]:
            sample = Sample.from_file(file, self.tag)
            sample.load_image()
            self.samples.append(sample)

    def load_samples(self):
        for sample in self.samples:
            sample.load_image()






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

    def load_image(self):
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