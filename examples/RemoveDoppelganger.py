import glob
from src.DoppengangerRemover import DoppelgangerRemover

target_folder = 'downloaded_images/'

categories = glob.glob(target_folder + "*")

folder_list = []
for cat in categories:
    print cat
    folder_list.append(cat + "/")

remover = DoppelgangerRemover.from_folder_list(folder_list)
doppelganger = remover.compare()
remover.clean()

print str(len(doppelganger)) + " images removed"
