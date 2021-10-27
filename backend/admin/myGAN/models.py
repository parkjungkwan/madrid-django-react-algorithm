'''
코랩에서 작동하는 코드 백업
https://github.com/rickiepark/handson-ml2/blob/master/17_autoencoders_and_gans.ipynb
'''
# %tensorflow_version 1.x
import os
# from utils.loaders import load_mnist
# from models.AE import Autoencoder
# from google.colab import drive
# drive.mount('/content/drive')
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.stats import norm
# from models.AE import Autoencoder
# from utils.loaders import load_mnist, load_model
import sys

from admin.common.models import ValueObject

assert sys.version_info >= (3, 5)

# Scikit-Learn ≥0.20 is required
import sklearn
assert sklearn.__version__ >= "0.20"
'''
try:
    # %tensorflow_version only exists in Colab.
    %tensorflow_version 2.x
    IS_COLAB = True
except Exception:
    IS_COLAB = False
'''
# TensorFlow ≥2.0 is required
import tensorflow as tf
from tensorflow import keras
assert tf.__version__ >= "2.0"
'''
if not tf.config.list_physical_devices('GPU'):
    print("No GPU was detected. LSTMs and CNNs can be very slow without a GPU.")
    if IS_COLAB:
        print("Go to Runtime > Change runtime and select a GPU hardware accelerator.")
'''
# Common imports
import numpy as np
import os

# to make this notebook's output stable across runs
np.random.seed(42)
tf.random.set_seed(42)

# To plot pretty figures
# %matplotlib inline
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rc('axes', labelsize=14)
mpl.rc('xtick', labelsize=12)
mpl.rc('ytick', labelsize=12)

# Where to save the figures
PROJECT_ROOT_DIR = "."
CHAPTER_ID = "autoencoders"
IMAGES_PATH = os.path.join(PROJECT_ROOT_DIR, "images", CHAPTER_ID)
os.makedirs(IMAGES_PATH, exist_ok=True)

class AutoencodersGans(object):
    def __init__(self):
        self.vo = ValueObject()
        self.vo.context = 'admin/myGAN/data/'

    def process(self):
        ctx = self.vo.context
        np.random.seed(4)
        X_train = self.generate_3d_data(60)
        X_train = X_train - X_train.mean(axis=0, keepdims=0)
        np.random.seed(42)
        tf.random.set_seed(42)

        encoder = keras.models.Sequential([keras.layers.Dense(2, input_shape=[3])])
        decoder = keras.models.Sequential([keras.layers.Dense(3, input_shape=[2])])
        autoencoder = keras.models.Sequential([encoder, decoder])

        autoencoder.compile(loss="mse", optimizer=keras.optimizers.SGD(learning_rate=1.5))
        history = autoencoder.fit(X_train, X_train, epochs=20)
        codings = encoder.predict(X_train)
        fig = plt.figure(figsize=(4, 3))
        plt.plot(codings[:, 0], codings[:, 1], "b.")
        plt.xlabel("$z_1$", fontsize=18)
        plt.ylabel("$z_2$", fontsize=18, rotation=0)
        plt.grid(True)
        plt.save_fig(f"{ctx}linear_autoencoder_pca_plot.png")
        # plt.show()

    def generate_3d_data(m, w1=0.1, w2=0.3, noise=0.1):
        angles = np.random.rand(m) * 3 * np.pi / 2 - 0.5
        '''
        TypeError: 'AutoencodersGans' object cannot be interpr
        eted as an integer
        '''
        data = np.empty((m, 3))
        data[:, 0] = np.cos(angles) + np.sin(angles) / 2 + noise * np.random.randn(m) / 2
        data[:, 1] = np.sin(angles) * 0.7 + noise * np.random.randn(m) / 2
        data[:, 2] = data[:, 0] * w1 + data[:, 1] * w2 + noise * np.random.randn(m)
        return data
'''
Stacked Autoencoders
'''
class GenerateFashion(object):
    def __init__(self):
        self.vo = ValueObject()
        self.vo.context = 'admin/myGAN/data/'

    def process(self):
        (X_train_full, y_train_full), (X_test, y_test) = keras.datasets.fashion_mnist.load_data()
        X_train_full = X_train_full.astype(np.float32) / 255
        X_test = X_test.astype(np.float32) / 255
        X_train, X_valid = X_train_full[:-5000], X_train_full[-5000:]
        y_train, y_valid = y_train_full[:-5000], y_train_full[-5000:]

        tf.random.set_seed(42)
        np.random.seed(42)

        stacked_encoder = keras.models.Sequential([
            keras.layers.Flatten(input_shape=[28, 28]),
            keras.layers.Dense(100, activation="selu"),
            keras.layers.Dense(30, activation="selu"),
        ])
        stacked_decoder = keras.models.Sequential([
            keras.layers.Dense(100, activation="selu", input_shape=[30]),
            keras.layers.Dense(28 * 28, activation="sigmoid"),
            keras.layers.Reshape([28, 28])
        ])
        stacked_ae = keras.models.Sequential([stacked_encoder, stacked_decoder])
        stacked_ae.compile(loss="binary_crossentropy",
                           optimizer=keras.optimizers.SGD(learning_rate=1.5),
                           metrics=[keras.metrics.binary_accuracy(tf.round(y_true), tf.round(y_pred))])
        history = stacked_ae.fit(X_train, X_train, epochs=20,
                                 validation_data=(X_valid, X_valid))
        self.show_reconstructions(stacked_ae)
        self.save_fig("reconstruction_plot")

    '''
    def rounded_accuracy(self, y_true, y_pred): # 135번 라인에 직접 입력함
        return keras.metrics.binary_accuracy(tf.round(y_true), tf.round(y_pred))'''

    def show_reconstructions(self, model, images=X_valid, n_images=5):
        reconstructions = model.predict(images[:n_images])
        fig = plt.figure(figsize=(n_images * 1.5, 3))
        for image_index in range(n_images):
            plt.subplot(2, n_images, 1 + image_index)
            self.plot_image(images[image_index])
            plt.subplot(2, n_images, 1 + n_images + image_index)
            self.plot_image(reconstructions[image_index])

    def save_fig(self, fig_id, tight_layout=True, fig_extension="png", resolution=300):
        IMAGES_PATH = self.vo.context
        path = os.path.join(IMAGES_PATH, fig_id + "." + fig_extension)
        print("Saving figure", fig_id)
        if tight_layout:
            plt.tight_layout()
        plt.savefig(path, format=fig_extension, dpi=resolution)

    def plot_image(self, image):
        plt.imshow(image, cmap="binary")
        plt.axis("off")

class MuseumFace(object):
    def __init__(self):
        pass

