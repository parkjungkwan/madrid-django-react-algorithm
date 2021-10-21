from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from admin.common.models import ValueObject
from admin.tensor.models import Perceptron


class Iris(object):
    def __init__(self):
        self.vo = ValueObject()
        self.vo.context = 'admin/iris/data/'

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
        clf = Perceptron(eta = 0.1, n_iter=10)
        self.draw_scatter(X)

    def draw_scatter(self, X):
        plt.scatter(X[:50, 0], X[:50, 1], color='red', marker='o', label='setosa')
        plt.scatter(X[50:100, 0], X[50:100, 1], color='blue', marker='x', label='versicolor')
        plt.xlabel('sepal length[cm]')
        plt.ylabel('petal length[cm]')
        plt.legend(loc='upper left')
        plt.savefig(f'{self.vo.context}iris_scatter.png')




