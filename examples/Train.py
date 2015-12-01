from src.Dataset import Dataset, CategorieInfo

#load dataset
cat_infos = []

echte_pfifferling = CategorieInfo.from_default("Echter Pfifferling/", [1,0,0])
falscher_pfifferling = CategorieInfo.from_default("Falscher Pfifferling/", [0,1,0])
fliegenpilz = CategorieInfo.from_default("fliegenpilz/", [0,0,1])

cat_infos.append(echte_pfifferling)
cat_infos.append(falscher_pfifferling)
cat_infos.append(fliegenpilz)

dataset = Dataset.from_sourcefolder("dataset1/")
dataset.categorie_infos = cat_infos
dataset.read_samples()
dataset.load_images()
trainset, testset = dataset.split_train_test(0.9)
