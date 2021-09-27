import h5py
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from keras.models import load_model
import cv2
from numpy import linalg
from extract_cnn_vgg16_keras import VGGNet
import sys
from PIL import Image
import io,os
import logging

logger = logging.getLogger(__name__)

def search_img(img_file,number):
    '''
    function:以图搜图
    image_file:待检索图片
    number:返回的图片id数
    '''
    # query = 'test_erhuan.jpg'
    # with open(img_file, 'rb') as f:
    #     a = f.read()
    byte_stream = io.BytesIO(img_file)
    
    img = Image.open(byte_stream)
    tmp = 'test.jpg'
    img.save(tmp)


    # category = 'feature/'
    # labels_list = ['bixi','chenxiang','erhuan','feicui','hetianyu','huanghuali','huanglongyu','jixueshi','jiezhi','manao',
    #     'mila','oubo','shouzhuo','xianglian','zhenzhu','zumulv','zuanshi']

    # # 判断检索图片类别
    # image = cv2.imread(query)
    # output = image.copy()
    # image = cv2.resize(output, (32, 32))
    # image = image.astype("float") / 255.0
    # image = image.reshape((1, image.shape[0], image.shape[1],image.shape[2]))
    # model = load_model('model/CNN.model')
    # preds = model.predict(image)
    # i = preds.argmax(axis=1)[0]
    # category = category + labels_list[i] + '.h5'

    # 读取数据集特征文件
    h5f = h5py.File('feature/product.h5', 'r')
    feats = h5f['dataset_1'][:]
    imgIds = h5f['dataset_2'][:]
    h5f.close()
    # queryImg = mpimg.imread(query)
    # plt.title("Query Image")
    # plt.imshow(queryImg)
    # plt.show()

    # 特征匹配
    model = VGGNet()
    queryVec = model.vgg_extract_feat(tmp)
    scores = np.dot(queryVec, feats.T)
    rank_ID = np.argsort(scores)[::-1]
    rank_score = scores[rank_ID]

    # 返回检索结果
    maxres = int(number)
    imlist = []
    for i, index in enumerate(rank_ID[0:maxres]):
        imlist.append(str(imgIds[index]))
        logger.info("image ids: " + str(imgIds[index]) + " scores: %f" % rank_score[i])
    logger.info("top %d images in order are: " % maxres, imlist)
    os.remove(tmp)
    # 显示检索图像
    # for i,im in enumerate(imlist):
    #     image = mpimg.imread(result + "/" +str(im,'utf-8'))
    #     plt.title("search output %d" % (i+1))
    #     plt.imshow(image)
    #     plt.show()
    return imlist

# 保存检索结果到result.txt
def save_result_txt(result):
    f = open('result.txt','w')
    for line in result:
        f.write(line[1:]+'\n')

if __name__ == '__main__':
    image,number = sys.argv[1], sys.argv[2]  # 第一个参数是图像url，第二个是需要返回的url数
    result = search_img(image, number)           # 以图搜图，返回列表
    save_result_txt(result)                       # 保存url到txt文件中