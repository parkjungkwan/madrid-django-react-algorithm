from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout
import tensorflow as tf
from admin.common.models import ValueObject, Reader
import os

class Iris(object):
    def __init__(self):
        self.vo = ValueObject()
        self.vo.context = 'admin/iris/data/'

    def iris_by_tf(self):
        reader = Reader()
        vo = self.vo
        train_dataset_url = "https://storage.googleapis.com/download.tensorflow.org/data/iris_training.csv"
        train_dataset_fp = tf.keras.utils.get_file(fname=os.path.basename(train_dataset_url),
                                                   origin=train_dataset_url)
        # print("Local copy of the dataset file: {}".format(train_dataset_fp)) # 파일 저장경로
        # print(f'type: {type(train_dataset_fp)}') # 해당 경로로 가서 data 폴더로 이동시킨다.
        vo.fname = 'iris_training'
        iris_df = reader.csv(reader.new_file(vo))
        # print(f'iris_df HEAD: {iris_df.head(3)}')
        # column order in CSV file
        column_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']

        feature_names = column_names[:-1]
        label_name = column_names[-1]

        print(f"Features: {feature_names}")
        print(f"Label: {label_name}")

        class_names = ['Iris setosa', 'Iris versicolor', 'Iris virginica']
        batch_size = 32

        train_dataset = tf.data.experimental.make_csv_dataset(
            train_dataset_fp,
            batch_size,
            column_names=column_names,
            label_name=label_name,
            num_epochs=1)
        features, labels = next(iter(train_dataset))

        print(features)
        plt.scatter(features['petal_length'],
                    features['sepal_length'],
                    c=labels,
                    cmap='viridis')

        plt.xlabel("Petal length")
        plt.ylabel("Sepal length")
        plt.savefig(f'{self.vo.context}iris_tf_scatter.png')

    def base(self):
        np.random.seed(0)
        iris = load_iris()
        iris_df = pd.DataFrame(iris.data, columns=iris.feature_names)
        # print(f'아이리스 데이터 구조: {iris_df.head(2)} \n {iris_df.columns}')
        '''
         ['sepal length (cm)', 꽃받침 
         'sepal width (cm)', 꽃받침 
         'petal length (cm)', 꽃잎
         'petal width (cm)'] 꽃잎
        '''
        iris_df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)
        # print(f'품종 추가된 아이리스 데이터 구조: {iris_df.head(2)} \n {iris_df.columns}')
        '''
        'sepal length (cm)', 'sepal width (cm)', 'petal length (cm)','petal width (cm)', 
        'species'
        '''
        iris_df['is_train'] = np.random.uniform(0, 1, len(iris_df)) <= 0.75 # train set 75%
        train, test = iris_df[iris_df['is_train'] == True], \
                      iris_df[iris_df['is_train'] == False]
        features = iris_df.columns[:4] # 0 ~ 3 까지 feature 추출
        # print(f'아이리스 features 값: {features} \n')
        y = pd.factorize(train['species'])[0]
        # print(f'아이리스 y 값: {y}') # 총 3종류의 품종이 있다
        # Learning
        clf = RandomForestClassifier(n_jobs=2, random_state=0)
        clf.fit(train[features], y)
        # print(clf.predict_proba(test[features])[0:10])
        # accuracy
        preds = iris.target_names[clf.predict(test[features])]
        # print(f'아이리스 crosstab 결과: {preds[0:5]} \n')
        # crosstab
        temp = pd.crosstab(test['species'], preds, rownames=['Actual Species'], colnames=['Predicted Species'])
        # print(f'아이리스 crosstab 결과: {temp} \n')
        '''
        0: setosa, 1: versicolor, 2: virginica
        '''
        # feature 별 중요도
        print(list(zip(train[features], clf.feature_importances_)))
        '''
        [('sepal length (cm)', 0.08474010289429795), 
        ('sepal width (cm)', 0.022461263894393204), 
        ('petal length (cm)', 0.4464851467243143), 
        ('petal width (cm)', 0.4463134864869946)]
        '''

    def advanced(self):
        iris = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data',
                                header=None)
        # 0: setosa, 1: versicolor
        iris_mini = iris.iloc[0:100, 4].values
        y = np.where(iris_mini == 'Iris-setosa', -1, 1)
        X = iris.iloc[0:100, [0,2]].values
        self.draw_scatter(X)


    def draw_scatter(self, X):
        plt.scatter(X[:50, 0], X[:50, 1], color='red', marker='o', label='setosa')
        plt.scatter(X[50:100, 0], X[50:100, 1], color='blue', marker='x', label='versicolor')
        plt.xlabel('sepal length[cm]')
        plt.ylabel('petal length[cm]')
        plt.legend(loc='upper left')
        plt.savefig(f'{self.vo.context}iris_scatter.png')






