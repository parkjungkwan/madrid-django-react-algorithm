from django.db import models
from admin.common.models import Dataset
import pandas as pd

class HousingService(object):

    dataset = Dataset()

    def new_model(self) -> object:
        return pd.read_csv('admin/housing/data/housing.csv')


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



