import math
import pandas_datareader as data_reader
import numpy as np
from tqdm import tqdm
import numpy as np
import tensorflow as tf
from collections import deque
import random

from admin.common.models import ValueObject
'''
pip install --upgrade pandas
pip install --upgrade pandas-datareader
'''

class AITrader(object):
    def __init__(self, action_space=3, model_name='AITrader'):
        self.vo = ValueObject()
        self.vo.context = 'admin/ai_trader/data/'
        self.state_size = 10 # windwo_size
        self.action_space = action_space
        self.memory = deque(maxlen=2000)
        self.inventory = []
        self.model_name = model_name
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_final = 0.01
        self.epsilon_decay = 0.995
        self.model = self.model_builder()

    def process(self):
        Trading().transaction('AAPL')

    def model_builder(self):
        model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(units=32, activation='relu', input_dim=self.state_size),
            tf.keras.layers.Dense(units=64, activation='relu'),
            tf.keras.layers.Dense(units=128, activation='relu'),
            tf.keras.layers.Dense(units=self.action_space, activation='linear'),
            tf.keras.layers.Dense(10, activation='softmax')
        ])
        model.compile(loss='mse', optimizer = tf.keras.optimizers.Adam(lr=0.001))
        return model


    def trade(self, state):
        if random.random() <= self.epsilon:
            return random.randrange(self.action_space)
        actions = self.model.predict(state)
        return np.argmax(actions[0])

    def batch_train(self, batch_size):
        model = self.model
        batch = []
        for i in range(len(self.memory) - batch_size + 1, len(self.memory)):
            batch.append(self.memory[i])
        for state,action, reward, next_state, done in batch:
            reward = reward
            if not done:
                reward = reward + self.gamma * np.amax(model.predict(next_state)[0])
            target = model.predict(state)
            target[0][action] = reward
            model.fit(state, target, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_final:
            self.epsilon *= self.epsilon_decay

class Trading:
    def __init__(self):
        pass

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))

    def stock_price_format(self, n):
        if n < 0:
            return "- $ {0:2f}".format(abs(n))
        else:
            return "$ {0:2f}".format(abs(n))

    def dataset_loader(self, stock_name):
        print(f'############# 2 : dataset_loader IN ############## {stock_name}')
        dataset = data_reader.DataReader(stock_name, data_source='yahoo')
        # start_date = str(dataset.index[0]).split()[0]
        # end_date = str(dataset.index[-1]).split()[0]
        close = dataset['Close']
        return close

    def state_creator(self, data, timestep, window_size):
        starting_id = timestep - window_size + 1
        if starting_id >= 0:
            windowed_data = data[starting_id: timestep + 1]
        else:
            windowed_data =- starting_id * [data[0]] + list(data[0:timestep + 1])

        state = []
        for i in range(window_size - 1):
            state.append(self.sigmoid((windowed_data[i + 1] - windowed_data[i])))
        return np.array([state])

    def transaction(self, stock_name):
        print(f'############# 1 : transaction IN ############## {stock_name}')
        data = self.dataset_loader(stock_name)
        print(f'############# 3 : dataset_loader OUT ############## {stock_name}')
        window_size = 10
        episodes = 100
        batch_size = 32
        data_samples = len(data) -1
        trader = AITrader(window_size)
        for episode in range(1, episodes + 1):
            print(f"Episode: {episode}/{episodes}")
            state = self.state_creator(data, 0, window_size + 1)
            total_profit = 0
            trader.inventory = []

            for t in tqdm(range(data_samples)):
                action = trader.trade(state)
                next_state = self.state_creator(data, t + 1, window_size + 1)
                reward = 0
                if action == 1: # Buying
                    trader.inventory.append(data[t])
                    print(f"AI 트레이더 매수: {self.stock_price_format(data[t])}")
                elif action == 2 and len(trader.inventory) > 0: # Selling
                    buy_price = trader.inventory.pop(0)
                    reward = max(data[t] - buy_price, 0)
                    total_profit += data[t] - buy_price
                    print("AI 트레이더 매도: ", self.stock_price_format(data[t]),
                          "이익: " + self.stock_price_format(data[t] - buy_price))
                if t == data_samples -1:
                    done = True
                else:
                    done = False

                trader.memory.append((state, action, reward, next_state, done))
                state = next_state

                if done:
                    print('#######################')
                    print(f'총이익: {total_profit}')
                    print('#######################')

                if len(trader.memory) > batch_size:
                    trader.batch_train(batch_size)

            if episode % 10 == 0:
                trader.model.save(f'{self.vo.context}ai_trader_{episode}.h5')






