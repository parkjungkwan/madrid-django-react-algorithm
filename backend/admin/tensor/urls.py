from django.conf.urls import url
from admin.tensor import views

urlpatterns = {
    url(r'calculator', views.calculator),
    url(r'fashion', views.fashion)
}
