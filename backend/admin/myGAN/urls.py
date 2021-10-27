from django.conf.urls import url
from admin.myGAN import views

urlpatterns = {
    url(r'autoencodersGans_process', views.autoencodersGans_process),

}
