from django.conf.urls import url
from admin.myNLP import views

urlpatterns = {
    url(r'imdb_process', views.imdb_process),

}
