import h5py
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import os

from extract_cnn_vgg16_keras import VGGNet

def get_imlist(path):
    return [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]

database = 'dataset/all'
index = 'feature/all.h5'
img_list = get_imlist(database)

feats = []
names = []

model = VGGNet()
for i, img_path in enumerate(img_list):
    norm_feat = model.vgg_extract_feat(img_path)
    img_name = os.path.split(img_path)[1]
    print(img_name)
    feats.append(norm_feat)
    names.append(img_name)

feats = np.array(feats)
output = index

h5f = h5py.File(output,'w')
h5f.create_dataset('dataset_1', data=feats)
h5f.create_dataset('dataset_2', data=np.string_(names))
h5f.close()