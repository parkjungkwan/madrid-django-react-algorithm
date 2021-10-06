from django.conf.urls import url
from admin.housing import views

urlpatterns = {
    url(r'police-position', views.housing_info),

}
