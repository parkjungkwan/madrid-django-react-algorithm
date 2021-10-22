from django.db import models
import pandas as pd
import os
import matplotlib.pyplot as plt
import mglearn
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
# Create your models here.
from admin.common.models import ValueObject
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import pandas_datareader.data as web
import numpy as np
from icecream import ic
import matplotlib.pyplot as plt
from fbprophet import Prophet
from datetime import datetime
from pandas_datareader import data
import math
import pandas_datareader as data_reader
from tqdm import tqdm
import numpy as np
import tensorflow as tf
from collections import deque
import random
import yfinance as yf
yf.pdr_override()
path = "c:/Windows/Fonts/malgun.ttf"
import platform
from matplotlib import font_manager, rc
if platform.system() == 'Darwin':
    rc('font', family='AppleGothic')
elif platform.system() == 'Windows':
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)
else:
    print('Unknown system... sorry~~~~')
plt.rcParams['axes.unicode_minus'] = False
'''
시계열 데이터 
: 일련의 순차적으로 정해진 데이터 셋의 집합
: 시간에 관해 순서가 매겨져 있다는 점과, 연속한 관측치는 서로 상관관계를 갖고 있다
회귀분석
: 관찰된 연속형 변수들에 대해 두 변수 사이의 모형을 구한뒤 적합도를 측정해 내는 분석 방법
'''

class MyRNN(object):
    def __init__(self):
        self.vo = ValueObject()
        self.vo.context = 'admin/rnn/data/'



    def kia_predict(self):
        start_date = '2018-1-4'
        end_date = '2021-9-30'
        KIA = data.get_data_yahoo('000270.KS', start_date, end_date)
        # print(KIA.head(3))
        # print(KIA.tail(3))
        KIA['Close'].plot(figsize=(12,6), grid=True)
        KIA_trunc = KIA[:'2021-12-31']
        df = pd.DataFrame({'ds': KIA_trunc.index, 'y': KIA_trunc['Close']})
        df.reset_index(inplace=True)
        del df['Date']
        print(f'df.head(3) 데이터: {df.head(3)}')
        prophet = Prophet(daily_seasonality=True)
        prophet.fit(df)
        future = prophet.make_future_dataframe(periods=61)
        print(f'future.tail(3) 데이터: {future.tail(3)}')
        forecast = prophet.predict(future)
        prophet.plot(forecast)
        plt.figure(figsize=(12,6))
        plt.plot(KIA.index, KIA['Close'], label='real')
        plt.plot(forecast['ds'], forecast['yhat'], label='forecase')
        plt.grid()
        plt.legend()
        plt.savefig(f'{self.vo.context}kia_close.png')

    def ram_price(self):
        ram_price = pd.read_csv(os.path.join(mglearn.datasets.DATA_PATH, "ram_price.csv"))
        plt.semilogy(ram_price.date, ram_price.price)
        plt.xlabel('year', size=15)
        plt.ylabel('price', size=15)
        # plt.savefig(f'{self.vo.context}ram_price.png')
        train = ram_price[ram_price['date'] < 2000] # 2000년 이전
        test = ram_price[ram_price['date'] >= 2000] # 2000년 이후
        x_train = train['date'][:, np.newaxis]
        y_train = np.log(train['price'])
        tree = DecisionTreeRegressor().fit(x_train, y_train)
        lr = LinearRegression().fit(x_train, y_train)
        x_all = ram_price['date'].values.reshape(-1, 1)
        pred_tree = tree.predict(x_all)
        price_tree = np.exp(pred_tree) # log 값 되돌리기
        pred_lr = lr.predict(x_all)
        price_lr = np.exp(pred_lr) # log 값 되돌리기
        plt.semilogy(ram_price['date'], pred_tree,
                     label="TREE PREDIC", ls='-', dashes=(2, 1))
        plt.semilogy(ram_price['date'], pred_lr,
                     label="LINEAR REGRESSION PREDIC", ls=':')
        plt.semilogy(train['date'], train['price'], label='TRAIN DATA', alpha=0.4)
        plt.semilogy(test['date'], test['price'], label='TEST DATA')
        plt.legend(loc=1)
        plt.xlabel('year', size=15)
        plt.ylabel('price', size=15)
        plt.savefig(f'{self.vo.context}ram_price_prediction.png')


