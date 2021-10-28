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
        pass
