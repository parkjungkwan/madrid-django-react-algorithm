import tensorflow as tf
import numpy as np


class Perceptron(object):

    def __init__(self, eta=0.01, n_iter=50, random_state=1):
        '''
        eta : float 학습률 (0.0과 1.0 사이)
        n_iter : int 훈련 데이터셋 반복 횟수
        random_state : int 가중치 무작위 초기화를 위한 난수 생성기
        '''
        self.eta = eta
        self.n_iter = n_iter
        self.random_state = random_state

    def fit(self, X, y) -> object: # 훈련데이터 학습
        '''
        w_ : 1d-array : 학습된 가중치
        errors_ : list 에포크마다 누적된 분류 오류
        '''
        rgen = np.random.RandomState(self.random_state)
        self.w_ = rgen.normal(loc=0.0, scale=0.01, size=1+X.shape[1])
        self.errors_ = []
        
        for _ in range(self.n_iter):
            errors = 0
            for xi, target in zip(X, y):
                update = self.eta * (target - self.predict(xi))
                self.w_[1:] += update * xi
                self.w_[0] += update
                errors += int(update != 0.0)
            self.errors_.append(errors)
        return self
        
    def predict(self, X): # 단위 계단 함수를 사용하여 클래스 레이블 반환
        return np.where(self.net_input(X) >= 0.0, 1, -1)

    def net_input(self, X): # 최종 입력 계산
        return np.dot(X, self.w_[1:]) + self.w_[0]

class Calculator(object):

    def __init__(self):
        print(f'Tensorflow Version: {tf.__version__}')

    def process(self):
        self.plus(4, 8)
        print('*'*100)
        self.mean()

    def plus(self, a, b):
        print(tf.constant(a) + tf.constant(b))

    def mean(self):
        x_array = np.arange(18).reshape(3,2,3)
        x2 = tf.reshape(x_array, shape=(-1, 6))
        # 각 열의 합을 계산
        xsum = tf.reduce_sum(x2, axis=0)
        # 각 열의 평균을 계산
        xmean = tf.reduce_mean(x2, axis=0)

        print(f'입력 크기: {x_array.shape} \n')
        print(f'크기가 변경된 입력 크기: {x2.numpy()}\n')
        print(f'열의 합: {xsum.numpy()}\n')
        print(f'열의 평균: {xmean.numpy()}\n')


