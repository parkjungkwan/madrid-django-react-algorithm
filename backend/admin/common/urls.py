from django.conf.urls import url
from admin.common import views

urlpatterns = {
    url(r'', views.connection)
}
