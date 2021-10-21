from django.conf.urls import url
from admin.myCV2 import views

urlpatterns = {
    url(r'lena', views.lena),
    url(r'girl', views.girl),
}
