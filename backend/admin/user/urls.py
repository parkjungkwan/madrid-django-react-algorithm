from django.conf.urls import url

from admin.user import views

urlpatterns = {
    url(r'^register', views.users),
    url(r'^list', views.users)
}
