from django.conf.urls import url
from admin.crime import views

urlpatterns = {
    url(r'police-position', views.create_police_position),

}
