import pandas as pd
import numpy as np 
import pickle #############
from sklearn.decomposition import PCA
from sklearn import preprocessing
import os
import cv2
from PIL import Image
import matplotlib.image as image


filename='yarab_nenga7_ya_tata7.sav'
def functionML(test , train):
    pca = pickle.load(open(filename, 'rb'))
    for i in range(1,4):
        globals()[f"train{i}"] = train[i-1].resize((320,243)).convert('L')
        globals()[f'train{i}'].save(f'train{i}.jpg')
        globals()[f"train{i}"] = image.imread(f'train{i}.jpg')
        globals()[f"train{i}"] = globals()[f'train{i}'].flatten()
    
    test = test.resize((320,243)).convert('L')
    test.save('test.jpg')
    test = image.imread('test.jpg')
    test = test.flatten()
    
    na_train = np.array((train1,train2, train3, test))

    train_scaled_dat = preprocessing.StandardScaler().fit_transform(na_train)
    pca_train = pca.transform(train_scaled_dat)

    distance = []
    for i in range(3):
        x = np.sum(np.sqrt(    (pca_train[3] - pca_train[i])**2    ))
        distance.append(x) 
    distances = np.array(distance)
    min_distance = (distances.min())
    if min_distance < 725 :
        print('welcome, sir')
        z = 1
    else : 
        print('please try again')
        z = 0
    return z