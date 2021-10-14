from django.db import models
import pandas as pd
import numpy as np
from admin.common.models import ValueObject
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedShuffleSplit
import matplotlib.pyplot as plt
from icecream import ic


class HousingService(object):

    def __init__(self):
        self.vo = ValueObject()
        self.vo.fname = 'admin/housing/data/housing.csv'
        self.model = self.vo.create_model()


    def housing_info(self):
        self.vo.model_info(self.model)

    def housing_hist(self):
        self.model.hist(bins=50, figsize=(20, 15))
        plt.savefig('admin/housing/image/housing-hist.png')

    def split_model(self) -> []:
        train_set, test_set = train_test_split(self.model, test_size=0.2, random_state=42)
        print('#'*100)
        self.vo.model_info(train_set)
        print('#' * 100)
        self.vo.model_info(test_set)
        return [train_set, test_set]

    def income_cat_hist(self):
        m = self.model
        m['income_cat'] = pd.cut(m['median_income'],
                                 bins=[0.,1.5,3.0,4.5,6.,np.inf], # np.inf is NaN(Not a Numer)
                                 labels=[1,2,3,4,5]
                                 )
        m['income_cat'].hist()
        plt.savefig('admin/housing/image/income-cat.png')

    def split_model_by_income_cat(self) -> []:
        m = self.model
        split = StratifiedShuffleSplit(n_splits=1, test=0.2, random_state=42)
        for train_idx, test_idx in split.split(m, m['income_cat']):
            temp_train_set = m.loc[train_idx]
            temp_test_set = m.loc[test_idx]
        ic(temp_test_set['income_cat'].value_counts() / len(temp_test_set))






class Housing(models.Model):

    housing_id = models.AutoField(primary_key=True)
    latitude = models.FloatField()
    housing_median_age = models.FloatField()
    total_rooms = models.FloatField()
    total_bedrooms = models.FloatField()
    population = models.FloatField()
    households = models.FloatField()
    median_income = models.FloatField()
    median_house_value = models.FloatField()
    ocean_proximity = models.TextField()

    class Meta:
        db_table = "housing"

    def __str__(self):
        return f'[{self.pk}] {self.housing_id}'


'''
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 20640 entries, 0 to 20639
Data columns (total 10 columns):
 #   Column              Non-Null Count  Dtype
---  ------              --------------  -----
 0   longitude           20640 non-null  float64
 1   latitude            20640 non-null  float64
 2   housing_median_age  20640 non-null  float64
 3   total_rooms         20640 non-null  float64
 4   total_bedrooms      20433 non-null  float64
 5   population          20640 non-null  float64
 6   households          20640 non-null  float64
 7   median_income       20640 non-null  float64
 8   median_house_value  20640 non-null  float64
 9   ocean_proximity     20640 non-null  object
dtypes: float64(9), object(1)
memory usage: 1.6+ MB

'''
