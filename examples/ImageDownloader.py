# -*- coding: utf-8 -*-
from src.GoogleImageExtractor import GoogleImageExtractor


falscherPfifferling = ["Falscher Pfifferling", "Hygrophoropsis aurantiaca"]
fliegenpilz = ["Amanita muscaria", "fly agaric"]
eierschwamme = ["Cantharellus cibarius", "Echter Pfifferling"]

keywords = eierschwamme
nb_images = 1000

for keyword in keywords:
    target_folder = 'downloaded_images/' + keyword + "/"
    extractor = GoogleImageExtractor.from_keyword(keyword, target_folder, nb_images)
    extractor.multi_search_download()