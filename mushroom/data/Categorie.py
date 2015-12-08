from SampleList import SampleList

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

    def read_samples(self):
        self.samples = SampleList.from_folder(self.sourcefolder, self.tag)





