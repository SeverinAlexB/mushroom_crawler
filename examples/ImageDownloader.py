# -*- coding: utf-8 -*-
from src.GoogleImageExtractor import GoogleImageExtractor

nb_images = 1000
keywords = ["Falscher Pfifferling", "Hygrophoropsis aurantiaca"]

for keyword in keywords:
    target_folder = 'downloaded_images/' + keyword + "/"
    extractor = GoogleImageExtractor.from_keyword(keyword, target_folder, nb_images)
    extractor.multi_search_download()