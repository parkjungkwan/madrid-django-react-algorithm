from django.conf.urls import url
from admin.ai_trader import views

urlpatterns = {

    url(r'process', views.process)
}
