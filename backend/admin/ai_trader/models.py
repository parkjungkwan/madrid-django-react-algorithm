import math
import pandas_datareader as data_reader
import numpy as np
from tqdm import tqdm
import numpy as np
import tensorflow as tf
from collections import deque
import random

from admin.common.models import ValueObject


class AITrader(object):
    def __init__(self, state_size, action_space=3, model_name='AITrader'):
        self.vo = ValueObject()
        self.vo.context = 'admin/ai_trader/data/'
        self.state_size = state_size
        self.action_space = action_space
        self.memory = deque(maxlen=2000)
        self.inventory = []
        self.model_name = model_name
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_final = 0.01
        self.epsilon_decay = 0.995
        self.model = self.model_builder()

    def model_builder(self):
        model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(units=32, activation='relu', input_dim=self.state_size),
            tf.keras.layers.Dropout(rate='0.2'),
            tf.keras.layers.Dense(units=64, activation='relu'),
            tf.keras.layers.Dropout(rate='0.2'),
            tf.keras.layers.Dense(units=128, activation='relu'),
            tf.keras.layers.Dropout(rate='0.2'),
            tf.keras.layers.Dense(units=self.action_space, activation='linear'),
            tf.keras.layers.Dropout(rate='0.2'),
            tf.keras.layers.Dense(10, activation='softmax')
        ])
        model.compile(loss='mse', optimizer = tf.keras.optimizers.Adam(lr=0.001))
        model.save(f'{self.vo.context}ai_trader.h5')


