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
        test_url = "https://storage.googleapis.com/download.tensorflow.org/data/iris_test.csv"

        test_fp = tf.keras.utils.get_file(fname=os.path.basename(test_url),
                                          origin=test_url)
        # print("Local copy of the dataset file: {}".format(train_dataset_fp)) # 파일 저장경로
        # print(f'type: {type(train_dataset_fp)}') # 해당 경로로 가서 data 폴더로 이동시킨다.
        vo.fname = 'iris_training'
        iris_df = reader.csv(reader.new_file(vo))
        # print(f'iris_df HEAD: {iris_df.head(3)}')
        # column order in CSV file
        column_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']

        feature_names = column_names[:-1]
        label_name = column_names[-1]

        # print(f"Features: {feature_names}")
        # print(f"Label: {label_name}")

        class_names = ['Iris setosa', 'Iris versicolor', 'Iris virginica']
        batch_size = 32

        train_dataset = tf.data.experimental.make_csv_dataset(
            train_dataset_fp,
            batch_size,
            column_names=column_names,
            label_name=label_name,
            num_epochs=1)
        features, labels = next(iter(train_dataset))

        # print(features)
        plt.scatter(features['petal_length'],
                    features['sepal_length'],
                    c=labels,
                    cmap='viridis')

        plt.xlabel("Petal length")
        plt.ylabel("Sepal length")
        # plt.savefig(f'{self.vo.context}iris_tf_scatter.png')

        test_dataset = tf.data.experimental.make_csv_dataset(
            test_fp,
            batch_size,
            column_names=column_names,
            label_name='species',
            num_epochs=1,
            shuffle=False)



        train_dataset = train_dataset.map(self.pack_features_vector)
        features, labels = next(iter(train_dataset))
        print(f'train_dataset features[:5] 의 값 : {features[:5]}')
        test_dataset = test_dataset.map(self.pack_features_vector)
        features, labels = next(iter(test_dataset))
        print(f'test_dataset features[:5] 의 값 : {features[:5]}')
        '''
        모델 타입 선정
        모델은 특성과 레이블 간의 관계입니다.
        좋은 머신러닝 접근 방식이라면 적절한 모델을 제시해 줍니다. 
        적절한 머신러닝 모델 형식에 충분한 대표 예제를 제공하면 프로그램이 관계를 파악해 줍니다.
        신경망에는 여러 범주가 있으며, 이 프로그램은 조밀(Dense)하거나 
        완전히 연결된 신경망(tf.nn)을 사용합니다. 
        '''
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(10, activation=tf.nn.relu, input_shape=(4,)),  # input shape required
            tf.keras.layers.Dense(10, activation=tf.nn.relu),
            tf.keras.layers.Dense(3)
        ])
        '''
        숨겨진 레이어에서는 주로 ReLU 함수가 사용됩니다.
        '''
        predictions = model(features)
        print(f'predictions[:5] 의 값 : {predictions[:5]}')
        print(f'tf.nn.softmax(predictions[:5]) 의 값 : {tf.nn.softmax(predictions[:5])}')
        print(f"tf.argmax(predictions, axis=1) 의 값 : {tf.argmax(predictions, axis=1)}")
        print(f"Labels의 값: {labels}")
        '''
        모델 훈련하기
        * 훈련 데이터세트에 대해 너무 많이 배우면 예측이 관측한 데이터에 대해서만 작동하고 
        일반화할 수 없습니다. 이런 문제를 과대적합(Overfitting)이라고 하며, 
        이는 문제를 해결하는 방법을 이해하는 대신 답을 암기하는 것과 같습니다.
        모델의 손실은 tf.keras.losses.categorical_crossentropy 함수를 사용해 계산합니다. 
        '''

        l = self.loss(model, features, labels, training=False)
        print(f"Loss test: {l}")
        '''
        옵티마이저는 계산된 그래디언트를 모델의 변수에 적용하여 loss 함수를 최소화합니다.
        loss 이 낮을수록 모델의 예측값이 더 좋습니다.
        '''
        optimizer = tf.keras.optimizers.SGD(learning_rate=0.01)
        loss_value, grads = self.grad(model, features, labels)

        print("Step: {}, Initial Loss: {}".format(optimizer.iterations.numpy(),
                                                  loss_value.numpy()))

        optimizer.apply_gradients(zip(grads, model.trainable_variables))

        print("Step: {},         Loss: {}".format(optimizer.iterations.numpy(),
                                                  self.loss(model, features, labels, training=True).numpy()))
        '''
        Epoch는 데이터세트를 통과시키는 횟수입니다.
        모델의 변수를 업데이트하기 위해 옵티마이저를 사용합니다.
        num_epochs 변수는 데이터세트 모음을 반복하는 횟수입니다.
        num_epochs는 조정할 수 있는 하이퍼 매개변수입니다. 
        적절한 횟수를 선택하는 것은 많은 경험과 직관을 필요로 합니다.
        '''
        ## Note: Rerunning this cell uses the same model variables

        # Keep results for plotting
        train_loss_results = []
        train_accuracy_results = []

        num_epochs = 201

        for epoch in range(num_epochs):
            epoch_loss_avg = tf.keras.metrics.Mean()
            epoch_accuracy = tf.keras.metrics.SparseCategoricalAccuracy()

            # Training loop - using batches of 32
            for x, y in train_dataset:
                # Optimize the model
                loss_value, grads = self.grad(model, x, y)
                optimizer.apply_gradients(zip(grads, model.trainable_variables))

                # Track progress
                epoch_loss_avg.update_state(loss_value)  # Add current batch loss
                # Compare predicted label to actual label
                # training=True is needed only if there are layers with different
                # behavior during training versus inference (e.g. Dropout).
                epoch_accuracy.update_state(y, model(x, training=True))

            # End epoch
            train_loss_results.append(epoch_loss_avg.result())
            train_accuracy_results.append(epoch_accuracy.result())

            if epoch % 50 == 0:
                print("Epoch {:03d}: Loss: {:.3f}, Accuracy: {:.3%}".format(epoch,
                                                                            epoch_loss_avg.result(),
                                                                            epoch_accuracy.result()))
        # 시간에 따른 손실함수 시각화
        fig, axes = plt.subplots(2, sharex=True, figsize=(12, 8))
        fig.suptitle('Training Metrics')

        axes[0].set_ylabel("Loss", fontsize=14)
        axes[0].plot(train_loss_results)

        axes[1].set_ylabel("Accuracy", fontsize=14)
        axes[1].set_xlabel("Epoch", fontsize=14)
        axes[1].plot(train_accuracy_results)
        plt.savefig(f'{self.vo.context}train_accuracy_results.png')

    def grad(self, model, inputs, targets):
        with tf.GradientTape() as tape:
            loss_value = self.loss(model, inputs, targets, training=True)
        return loss_value, tape.gradient(loss_value, model.trainable_variables)

    def loss(self, model, x, y, training):
        loss_object = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
        # training=training is needed only if there are layers with different
        # behavior during training versus inference (e.g. Dropout).
        y_ = model(x, training=training)

        return loss_object(y_true=y, y_pred=y_)

    def pack_features_vector(self, features, labels):
        """Pack the features into a single array."""
        features = tf.stack(list(features.values()), axis=1)
        return features, labels

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






