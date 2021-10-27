# CPU 처리
# 문제 있음 : 마지막에 그래프가 그려지지 않음

# import tensorflow.compat.v1 as tf
# tf.disable_v2_behavior()
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import matplotlib.pyplot as plt
from tensorflow.python.keras import datasets
from tensorflow import keras
import tensorflow as tf
# print(f'{tf.__version__}')

class CatDogClassification(object):

    def __init__(self):
        pass

    def process(self):
        batch_size = 128
        epochs = 1  # 시간절약
        IMG_HEIGHT = 150
        IMG_WIDTH = 150
        train_dir = None
        validation_dir = None
        train_cats_dir = None
        train_dogs_dir = None
        validation_cats_dir = None
        validation_dogs_dir = None
        train_data_gen = None
        total_train = None
        total_val = None
        val_data_gen = None
        (train_images, train_labels), (test_images, test_labels) = datasets.mnist.load_data()
        train_images = train_images.reshape((60000, 28, 28, 1))
        test_images = test_images.reshape((10000, 28, 28, 1))
        # 픽셀 값을 0~1 사이로 정규화합니다.
        train_images, test_images = train_images / 255.0, test_images / 255.0
        _URL = 'https://storage.googleapis.com/mledu-datasets/cats_and_dogs_filtered.zip'
        path_to_zip = tf.keras.utils.get_file('cats_and_dogs.zip', origin=_URL, extract=True)
        PATH = os.path.join(os.path.dirname(path_to_zip), 'cats_and_dogs_filtered')
        train_dir = os.path.join(PATH, 'train')
        validation_dir = os.path.join(PATH, 'validation')
        train_cats_dir = os.path.join(train_dir, 'cats')  # directory with our training cat pictures
        train_dogs_dir = os.path.join(train_dir, 'dogs')  # directory with our training dog pictures
        validation_cats_dir = os.path.join(validation_dir, 'cats')  # directory with our validation cat pictures
        validation_dogs_dir = os.path.join(validation_dir, 'dogs')  # directory with our validation dog pictures
        num_cats_tr = len(os.listdir(train_cats_dir))
        num_dogs_tr = len(os.listdir(train_dogs_dir))
        num_cats_val = len(os.listdir(validation_cats_dir))
        num_dogs_val = len(os.listdir(validation_dogs_dir))
        total_train = num_cats_tr + num_dogs_tr
        total_val = num_cats_val + num_dogs_val
        print('total training cat images:', num_cats_tr)
        print('total training dog images:', num_dogs_tr)
        print('total validation cat images:', num_cats_val)
        print('total validation dog images:', num_dogs_val)
        print("--")
        print("Total training images:", total_train)
        print("Total validation images:", total_val)
        model = Sequential([
            Conv2D(16, 3, padding='same',
                   activation='relu',
                   input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
            MaxPooling2D(),
            Conv2D(32, 3, padding='same', activation='relu'),
            MaxPooling2D(),
            Conv2D(64, 3, padding='same', activation='relu'),
            MaxPooling2D(),
            Flatten(),
            Dense(512, activation='relu'),
            Dense(1, activation='sigmoid')
        ])
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        print('---------- MODEL SUMMARY -------------')
        print(model.summary())
        model.save('cats_and_dogs.h5')
        print('======= 모델 훈련 종료 ======')
        history = self.train_model()
        acc = history.history['acc']
        val_acc = history.history['val_acc']
        loss = history.history['loss']
        val_loss = history.history['val_loss']
        epochs_range = range(1)  # epochs 1은 시간절약
        plt.figure(figsize=(8, 8))
        plt.subplot(1, 2, 1)
        plt.plot(epochs_range, acc, label='Training Accuracy')
        plt.plot(epochs_range, val_acc, label='Validation Accuracy')
        plt.legend(loc='lower right')
        plt.title('Training and Validation Accuracy')
        plt.subplot(1, 2, 2)
        plt.plot(epochs_range, loss, label='Training Loss')
        plt.plot(epochs_range, val_loss, label='Validation Loss')
        plt.legend(loc='upper right')
        plt.title('Training and Validation Loss')
        # plt.show()
        plt.savefig(f'{self.vo.context}cat_dog_classification.png')

    def train_model(self):
        print('케라스에서 모델 호출')
        model = keras.models.load_model('cats_and_dogs.h5')
        history = model.fit_generator(self.train_data_gen,
                                      steps_per_epoch=self.total_train // self.batch_size,
                                      epochs=1,
                                      validation_data=self.val_data_gen,
                                      validation_steps=self.total_val // self.batch_size
                                      )
        return history


