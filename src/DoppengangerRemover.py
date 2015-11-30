from PIL import Image
import os
import glob

class DoppelgangerRemover:
    def __init__(self):
        self.folder_list = []
        self.doppelganger = []

    @classmethod
    def from_folder_list(cls, folder_list):
        remover = cls()
        remover.folder_list = folder_list
        return remover

    def _get_image_list(self):
        files = []
        for folder in self.folder_list:
           files += glob.glob(folder + "*.*")

        return files

    def compare(self):
        file_list = self._get_image_list()
        hashs = self._generate_hash_dict(file_list)

        doppelganger = []

        while(len(file_list) > 0):
            current_doppel = []
            current = file_list[0]
            current_hash = hashs[current]
            for other in file_list:
                other_hash = hashs[other]
                if current == other:
                    continue
                if current_hash == other_hash:
                    current_doppel.append(other)

            for doppel in current_doppel:
                file_list.remove(doppel)
            file_list.remove(current)
            doppelganger += current_doppel

        self.doppelganger = doppelganger
        return doppelganger

    def clean(self):
        for doppel in self.doppelganger:
            os.remove(doppel)

    def _generate_hash_dict(self, file_list):
        hashs = {}

        for file in file_list:
            hashs[file] = self._generate_hash(file)
        return hashs


    def _generate_hash(self, filepath):
        try:
            img = Image.open(filepath)
            return self.dhash(img)
        except Exception as e:
            return ""

    def dhash(self, image, hash_size = 8):
        # Grayscale and shrink the image in one step.
        image = image.convert('L').resize(
            (hash_size + 1, hash_size),
            Image.ANTIALIAS,
        )

        pixels = list(image.getdata())

        # Compare adjacent pixels.
        difference = []
        for row in xrange(hash_size):
            for col in xrange(hash_size):
                pixel_left = image.getpixel((col, row))
                pixel_right = image.getpixel((col + 1, row))
                difference.append(pixel_left > pixel_right)

        # Convert the binary array to a hexadecimal string.
        decimal_value = 0
        hex_string = []
        for index, value in enumerate(difference):
            if value:
                decimal_value += 2**(index % 8)
            if (index % 8) == 7:
                hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
                decimal_value = 0

        return ''.join(hex_string)