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
import numpy as np
# print(f'{tf.__version__}')

class Cifar10Classification(object):
    def __init__(self):
        pass

    def process(self):
        (X_train, y_train), (X_test, y_test) = keras.datasets.cifar10.load_data()
        class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog',
                       'horse', 'ship', 'truck']
        X_train = X_train / 255.0
        X_test = X_test / 255.0
        plt.imshow(X_test[10])
        # plt.show()
        plt.savefig(f'{self.vo.context}cifar10_classification.png')
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, padding='same', activation='relu',
                                         input_shape=[32, 32, 3]))
        model.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, padding='same', activation='relu'))
        model.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2, padding='valid'))
        model.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, padding='same', activation='relu'))
        model.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, padding='same', activation='relu'))
        model.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2, padding='valid'))
        model.add(tf.keras.layers.Flatten())
        model.add(tf.keras.layers.Dense(units=128, activation='relu'))
        model.add(tf.keras.layers.Dense(units=10, activation='softmax'))
        print(model.summary())
        model.compile(loss='sparse_categorical_crossentropy',
                      optimizer='Adam',
                      metrics=['sparse_categorical_accuracy'])
        model.fit(X_train, y_train, epochs=3)
        test_loss, test_accuracy = model.evaluate(X_test, y_test)
        print('테스트 정확도: {}'.format(test_accuracy))
        '''
        # 
        '''
        # 인풋 아웃풋 데이터, 드롭아웃 확률을 입력받기위한 플레이스홀더를 정의합니다.
        x = tf.placeholder(tf.float32, shape=[None, 32, 32, 3])
        y = tf.placeholder(tf.float32, shape=[None, 10])
        keep_prob = tf.placeholder(tf.float32)
        # Convolutional Neural Networks(CNN) 그래프를 생성합니다.
        y_pred, logits = self.build_CNN_classifier(x)
        # Cross Entropy를 비용함수(loss function)으로 정의하고, RMSPropOptimizer를 이용해서 비용 함수를 최소화합니다.
        loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=logits))
        train_step = tf.train.RMSPropOptimizer(1e-3).minimize(loss)
        # 정확도를 계산하는 연산을 추가합니다.
        correct_prediction = tf.equal(tf.argmax(y_pred, 1), tf.argmax(y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        from tensorflow.keras.datasets.cifar10 import load_data
        import numpy as np
        # CIFAR-10 데이터를 다운로드하고 데이터를 불러옵니다.
        (x_train, y_train), (x_test, y_test) = load_data()
        # scalar 형태의 레이블(0~9)을 One-hot Encoding 형태로 변환합니다.
        y_train_one_hot = tf.squeeze(tf.one_hot(y_train, 10), axis=1)
        y_test_one_hot = tf.squeeze(tf.one_hot(y_test, 10), axis=1)
        # 세션을 열어 실제 학습을 진행합니다.
        with tf.Session() as sess:
            # 모든 변수들을 초기화한다.
            sess.run(tf.global_variables_initializer())
            # 10000 Step만큼 최적화를 수행합니다.
            for i in range(10000):
                batch = self.next_batch(128, X_train, y_train_one_hot.eval())
                # 100 Step마다 training 데이터셋에 대한 정확도와 loss를 출력합니다.
                if i % 100 == 0:
                    train_accuracy = accuracy.eval(feed_dict={x: batch[0], y: batch[1], keep_prob: 1.0})
                    loss_print = loss.eval(feed_dict={x: batch[0], y: batch[1], keep_prob: 1.0})
                    print("반복(Epoch): %d, 트레이닝 데이터 정확도: %f, 손실 함수(loss): %f" % (i, train_accuracy, loss_print))
                # 20% 확률의 Dropout을 이용해서 학습을 진행합니다.
                sess.run(train_step, feed_dict={x: batch[0], y: batch[1], keep_prob: 0.8})
            # 학습이 끝나면 테스트 데이터(10000개)에 대한 정확도를 출력합니다.
            test_accuracy = 0.0
            for i in range(10):
                test_batch = self.next_batch(1000, x_test, y_test_one_hot.eval())
                test_accuracy = test_accuracy + accuracy.eval(
                    feed_dict={x: test_batch[0], y: test_batch[1], keep_prob: 1.0})
            test_accuracy = test_accuracy / 10;
            print("테스트 데이터 정확도: %f" % test_accuracy)

    def next_batch(self, num, data, labels):
        # num 갯수 만큼 랜덤한 샘플들과 레이블들을 리턴
        idx = np.arange(0, len(data))
        np.random.shuffle(idx)
        idx = idx[:num]
        data_shuffle = [data[i] for i in idx]
        labels_shuffle = [labels[i] for i in idx]
        return np.asarray(data_shuffle), np.asarray(labels_shuffle)

    def build_CNN_classifier(self, x):
        # 입력이미지
        x_image = x
        # 첫번째 컨볼루션 레이어 - 하나의 그레이스케일 이미지를 64개의 특징으로 맵핑한다.
        W_conv1 = tf.Variable(tf.truncated_normal(shape=[5, 5, 3, 64], stddev=5e-2))
        b_conv1 = tf.Variable(tf.constant(0.1, shape=[64]))
        h_conv1 = tf.nn.relu(tf.nn.conv2d(x_image, W_conv1, strides=[1, 1, 1, 1], padding='SAME') + b_conv1)
        # 첫번째 pool layer
        h_pool1 = tf.nn.max_pool(h_conv1, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME')
        # 두번째 컨볼루션 레이어: 32개의 특징들(feature)을 64개의 특징들로 맵핑한다
        W_conv2 = tf.Variable(tf.truncated_normal(shape=[5, 5, 3, 64], stddev=5e-2))
        b_conv2 = tf.Variable(tf.constant(0.1, shape=[64]))
        h_conv2 = tf.nn.relu(tf.nn.conv2d(x_image, W_conv1, strides=[1, 1, 1, 1], padding='SAME') + b_conv1)
        # 두번째 pooling layer.
        h_pool2 = tf.nn.max_pool(h_conv2, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME')
        # 세번째 convolutional layer
        W_conv3 = tf.Variable(tf.truncated_normal(shape=[3, 3, 64, 128], stddev=5e-2))
        b_conv3 = tf.Variable(tf.constant(0.1, shape=[128]))
        h_conv3 = tf.nn.relu(tf.nn.conv2d(h_pool2, W_conv3, strides=[1, 1, 1, 1], padding='SAME') + b_conv3)
        # 네번째 convolutional layer
        W_conv4 = tf.Variable(tf.truncated_normal(shape=[3, 3, 128, 128], stddev=5e-2))
        b_conv4 = tf.Variable(tf.constant(0.1, shape=[128]))
        h_conv4 = tf.nn.relu(tf.nn.conv2d(h_conv3, W_conv4, strides=[1, 1, 1, 1], padding='SAME') + b_conv4)
        # 다섯번째 convolutional layer
        W_conv5 = tf.Variable(tf.truncated_normal(shape=[3, 3, 128, 128], stddev=5e-2))
        b_conv5 = tf.Variable(tf.constant(0.1, shape=[128]))
        h_conv5 = tf.nn.relu(tf.nn.conv2d(h_conv4, W_conv5, strides=[1, 1, 1, 1], padding='SAME') + b_conv5)
        # Fully Connected Layer 1 - 2번의 downsampling 이후에, 우리의 32x32 이미지는 8x8x128 특징맵(feature map)이 됩니다.
        # 이를 384개의 특징들로 맵핑(maping)합니다.
        W_fc1 = tf.Variable(tf.truncated_normal(shape=[8 * 8 * 128, 384], stddev=5e-2))
        b_fc1 = tf.Variable(tf.constant(0.1, shape=[384]))
        h_conv5_flat = tf.reshape(h_conv5, [-1, 8 * 8 * 128])
        h_fc1 = tf.nn.relu(tf.matmul(h_conv5_flat, W_fc1) + b_fc1)
        # Dropout - 모델의 복잡도를 컨트롤합니다. 특징들의 co-adaptation을 방지합니다.
        h_fc1_drop = tf.nn.dropout(h_fc1, self.keep_prob)
        # Fully Connected Layer 2 - 384개의 특징들(feature)을 10개의 클래스-airplane, automobile, bird...-로 맵핑(maping)합니다.
        W_fc2 = tf.Variable(tf.truncated_normal(shape=[384, 10], stddev=5e-2))
        b_fc2 = tf.Variable(tf.constant(0.1, shape=[10]))
        logits = tf.matmul(h_fc1_drop, W_fc2) + b_fc2
        y_pred = tf.nn.softmax(logits)
        return y_pred, logits

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


