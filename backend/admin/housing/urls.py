from django.conf.urls import url
from admin.housing import views

urlpatterns = {
    url(r'', views.housing)
}
