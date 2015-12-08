# -*- coding: utf-8 -*-
from mushroom.GoogleImageExtractor import GoogleImageExtractor


falscherPfifferling = ["Falscher Pfifferling", "Hygrophoropsis aurantiaca"]
fliegenpilz = ["Amanita muscaria", "fly agaric"]
eierschwamme = ["Cantharellus cibarius", "Echter Pfifferling"]
done = ["Agrocybe praecox", "Hericium ramosum", "Tremelia encephala", "Cystoderma amianthinum",
           "Sclerotinia tuberosa", "Agaricus arvensis", "Pleurotus ostreatus", "Aleuria aurantia",
           "Leccinum scabrum", "Leeccinum versipelle", "Russula aeruginea", "Lycoperdon pyriforme",
           "Gyromitra infula", "Tremella foliacea"]
one_cat = [ "Spongiporus caesius", "Lycogala epidendrum",
           "Megacollybia platyphylla", "Neobulgaria pura", "Oudemansiella mucida", "Suillus luteus",
           "Geoglossum cookeianum", "Pluteus leoninus", "Fistulina hepatica", "Lactarius quietus",
           "Panellus stipticus", "Ciboria aurentacea", "Otidea onotica", "Leecinum rufum",
           "Phellinus igniarius", "Lactarius deterrimus", "Strobilurus esculentus", "Lactarius helvus"]

keywords = one_cat
nb_images = 500

for keyword in keywords:
    target_folder = 'downloaded_images/' + keyword + "/"
    print target_folder
    extractor = GoogleImageExtractor.from_keyword(keyword, target_folder, nb_images)
    extractor.multi_search_download()