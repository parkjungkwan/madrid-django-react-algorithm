from django.test import TestCase

# Create your tests here.
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import matplotlib.pyplot as plt
from tensorflow.python.keras import datasets
from tensorflow import keras
print(f'{tf.__version__}')

if __name__ == '__main__':
    # 방법1 range()
    dc1 = {}
    dc2 = {}
    dc3 = {}
    ls1 = ['10', '20', '30', '40', '50']
    ls2 = [10, 20, 30, 40, 50]
    # for i in range(0, len(ls1)):
    #     dc1[ls1[i]] = ls2[i]
    dc1 = {ls1[i]:ls2[i] for i in range(0, len(ls1))}
    # 방법 zip()
    # for i, j in zip(ls1, ls2):
    #     dc2[i] = j
    dc2 = {i:j for i, j in zip(ls1, ls2)}
    # 방법 enumerate()
    # for i, j in enumerate(ls1):
    #     dc3[j] = ls2[i]
    dc3 = {j:ls2[i] for i, j in enumerate(ls1)}
    print('*'*30)
    print(dc1)
    print('*' * 30)
    print(dc2)
    print('*' * 30)
    print(dc3)
