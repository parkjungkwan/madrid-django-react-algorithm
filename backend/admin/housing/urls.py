from django.conf.urls import url
from admin.housing import views

urlpatterns = {
    url(r'housing-info', views.housing_info),
    url(r'housing-hist', views.housing_hist),
    url(r'split-model', views.split_model),
    url(r'income-cat-hist', views.income_cat_hist),
    url(r'split-model-by-income-cat', views.split_model_by_income_cat)
}
