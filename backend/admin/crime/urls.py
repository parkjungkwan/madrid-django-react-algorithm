from django.conf.urls import url
from admin.crime import views

urlpatterns = {
    url(r'police-position', views.create_police_position),
    url(r'cctv-model', views.create_cctv_model),
    url(r'population-model', views.create_population_model),
    url(r'merge-cctv-pop', views.merge_cctv_pop),
    url(r'process', views.process),



}
