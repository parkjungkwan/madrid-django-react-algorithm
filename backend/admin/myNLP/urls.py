from django.conf.urls import url
from admin.myNLP import views

urlpatterns = {
    url(r'imdb_process', views.imdb_process),
    url(r'naver_process', views.naver_process),

}
