from django.conf.urls import url
from admin.myCV2 import views

urlpatterns = {
    url(r'lena', views.lena),
    url(r'girl', views.girl),
    url(r'face_detect', views.face_detect),
    url(r'cat_mosaic', views.cat_mosaic),

}
