import os
import h5py
import sys
import numpy as np
from extract_cnn_vgg16_keras import VGGNet
from PIL import Image
import io
import logging

logger = logging.getLogger(__name__)

def create_feature_file(feat,name):
    h5f = h5py.File('feature/product.h5','w')
    h5f.create_dataset('dataset_1', data=feat)
    h5f.create_dataset('dataset_2', data=np.string_(name.tolist()))
    h5f.close()

def create_feature_file_2(feat,name):
    h5f = h5py.File('feature/product.h5','w')
    h5f.create_dataset('dataset_1', data=feat)
    h5f.create_dataset('dataset_2', data=np.str(name[0]))
    h5f.close()

def save_feature(img_file, id):
    model = VGGNet()

    # with open(img_file, 'rb') as f:
    #     img_file = f.read()
    byte_stream = io.BytesIO(img_file)
    
    img = Image.open(byte_stream)
    tmp = 'test.jpg'
    img.save(tmp)

    feat_1 = model.vgg_extract_feat(tmp)
    name_1 = id
    
    if os.path.exists('feature/product.h5'):
        h5f = h5py.File('feature/product.h5','a')
        feat_2 = h5f['dataset_1'][:]
        name_2 = h5f['dataset_2'][()]
        h5f.close()
        os.remove('feature/product.h5')
        feat = np.vstack((feat_2,feat_1))
        name = np.append(name_2,name_1)
        create_feature_file(feat,name)
    else:
        feat,name = [],[]
        feat.append(feat_1)
        name.append(name_1)
        feat = np.array(feat)
        create_feature_file_2(feat,name)
    os.remove(tmp)
    logger.info("feature saved")

if __name__ == "__main__":
    img_file,id = sys.argv[1], sys.argv[2]
    save_feature(img_file,id)


    # 以下部分为测试信息，查看新商品图片特征和名称是否插入h5文件，测试通过后可删除以下内容
    # h5f = h5py.File('feature/product.h5','r')
    # feat = h5f['dataset_1'][:]
    # name = h5f['dataset_2'][:]
    # h5f.close()
    # logger.info(feat)
    # logger.info(name)