# -*- coding: utf-8 -*-
from src.GoogleImageExtractor import GoogleImageExtractor

keyword = u"лисички лес"
target_folder = 'downloaded_images/' + keyword + "/"
nb_images = 1000

extractor = GoogleImageExtractor.from_keyword(keyword, target_folder, nb_images)
extractor.multi_search_download()