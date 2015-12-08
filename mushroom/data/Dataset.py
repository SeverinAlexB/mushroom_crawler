import numpy as np
from random import shuffle
from Categorie import Categorie
from TagManager import TagManager
from SampleList import SampleList
import glob

class Dataset:
    def __init__(self):
        self.sourcefolder = None
        self.categories = []
        self.tagmanager = None
        self.samples_shuffled = SampleList()

    @classmethod
    def from_sourcefolder(cls, sourcefolder):
        set = cls()
        set.sourcefolder = sourcefolder
        set._read_categories()
        return set

    def _read_categories(self):
        folders = glob.glob(self.sourcefolder + "*")
        nb_categories = len(folders)
        self.tagmanager = TagManager.from_nb_tags(nb_categories)
        for folder in folders:
            cat_folder = folder + "/"
            tag = self.tagmanager.get_tag(cat_folder)
            cat = Categorie.from_default(cat_folder, tag)
            self.categories.append(cat)


    def read_samples(self):
        for cat in self.categories:
            cat.read_samples()

        for cat in self.categories:
            self.samples_shuffled += cat.samples

        shuffle(self.samples_shuffled)





