from math import log, exp
from collections import defaultdict
import math
import numpy as np
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
from selenium import webdriver
from bs4 import BeautifulSoup
import csv
from admin.common.models import ValueObject
import pandas as pd

class NaverMovie(object):

    def __init__(self):
        self.vo = ValueObject()
        self.vo.context = 'admin/myNLP/data/'
        self.k = 0.5
        self.word_probs = []

    def naver_process(self):
        n = NaverMovie()
        n.model_fit()
        result = n.classify('내 인생 최고의 영화') # 0.9634566316047457
        print(f'결과 :::: {result}')
        result = n.classify('시간 아깝다. 정말 쓰레기다') #  0.00032621763187734896
        print(f'결과 :::: {result}')
        result = n.classify('평범하다, 배우들 연기가 조금 아쉽다')
        print(f'결과 :::: {result}')
        print('#'*100)

    def load_corpus(self):
        corpus = pd.read_table(f'{self.vo.context}review_train.csv', sep=',', encoding='UTF-8')
        corpus = np.array(corpus)
        return corpus

    def count_words(self, train_X):
        counts = defaultdict(lambda: [0, 0])
        for doc, point in train_X:
            if self.isNumber(doc) is False:
                words = doc.split()
                for word in words:
                    counts[word][0 if point > 3.5 else 1] += 1
        return counts


    def isNumber(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False


    def word_probabilities(self, counts, n_class0, n_class1, k):
        return [(w,
                 (class0 + k) / (n_class0 + 2 * k),
                 (class1 + k) / (n_class1 + 2 * k))
                for w, (class0, class1) in counts.items()]


    def probability(self, word_probs, doc):
        docwords = doc.split()
        log_prob_if_class0 = log_prob_if_class1 = 0.0
        for word, prob_if_class0, prob_if_class1 in word_probs:
            if word in docwords:
                log_prob_if_class0 += log(prob_if_class0)
                log_prob_if_class1 += log(prob_if_class1)
            else:
                log_prob_if_class0 += log(1.0 - prob_if_class0)
                log_prob_if_class1 += log(1.0 - prob_if_class1)
        prob_if_class0 = exp(log_prob_if_class0)
        prob_if_class1 = exp(log_prob_if_class1)
        return prob_if_class0 / (prob_if_class0 + prob_if_class1)


    def model_fit(self):
        train_X = self.load_corpus()
        '''
        '재밋었네요': [1, 0]
        '별로재미없다': [0, 1]
        '''
        num_class0 = len([1 for _, point in train_X if point > 3.5])
        num_class1 = len(train_X) - num_class0
        word_counts = self.count_words(train_X)
        self.word_probs = self.word_probabilities(word_counts, num_class0, num_class1, self.k)

    def classify(self, doc):
        return self.probability(self.word_probs, doc)


class MyImdb(object):
    def __init__(self):
        self.vo = ValueObject()
        self.vo.context = 'admin/myNLP/data/'

    def decode_review(self, text, reverse_word_index):
        return ' '.join([reverse_word_index.get(i, '?') for i in text])

    def imdb_process(self):
        imdb = keras.datasets.imdb

        (train_X, train_Y), (test_X, test_Y) = imdb.load_data(num_words=10000)
        print(f'>>>>>{type(train_X)}')

        word_index = imdb.get_word_index()
        word_index = {k: (v + 3) for k, v in word_index.items()}
        word_index["<PAD>"] = 0
        word_index["<START>"] = 1
        word_index["<UNK>"] = 2  # Unknown
        word_index["<UNUSED>"] = 3
        train_X = keras.preprocessing.sequence.pad_sequences(train_X,
                                                             value=word_index['<PAD>'],
                                                             padding='post',
                                                             maxlen=256)
        test_X = keras.preprocessing.sequence.pad_sequences(test_X,
                                                            value=word_index['<PAD>'],
                                                            padding='post',
                                                            maxlen=256)
        vacab_size = 10000
        model = keras.Sequential()
        model.add(keras.layers.Embedding(vacab_size, 16, input_shape=(None,)))
        model.add(keras.layers.GlobalAvgPool1D())
        model.add(keras.layers.Dense(16, activation=tf.nn.relu))
        model.add(keras.layers.Dense(1, activation=tf.nn.sigmoid))
        model.compile(optimizer=tf.optimizers.Adam(), loss='binary_crossentropy', metrics=['acc'])
        x_val = train_X[:10000]
        partial_X_train = train_X[10000:]
        y_val = train_Y[:10000]
        partial_Y_train = train_Y[10000:]
        history = model.fit(partial_X_train, partial_Y_train, epochs=40, batch_size=512, validation_data=(x_val, y_val))
        result = model.evaluate(test_X, test_Y)
        print(f'정확도 ::: {result}')
        '''
        loss: 0.0880 - 
        acc: 0.9785 - 
        val_loss: 0.3153 - 
        val_acc: 0.8819
        '''
        history_dict = history.history
        history_dict.keys()
        acc = history_dict['acc']
        val_acc = history_dict['val_acc']
        # loss = history_dict['loss']
        # val_loss = history_dict['val_loss']
        epochs = range(1, len(acc) + 1)
        plt.plot(epochs, acc, 'bo', label='Training acc')
        plt.plot(epochs, val_acc, 'b', label='Validation acc')
        plt.title('Training and validation accuracy')
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy')
        plt.legend()
        plt.savefig(f'{self.vo.context}imdb_nlp.png')