from django.conf.urls import url

from admin.common import views
from django.urls import path, include
urlpatterns = {
    path('', views.connection)
}
