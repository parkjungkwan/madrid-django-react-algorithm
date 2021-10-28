from django.conf.urls import url

from admin.user import views

urlpatterns = {
    url(r'', views.users, name='users'),
    url(r'', views.users),
    url(r'', views.users),
    url(r'', views.users),
    url(r'', views.users),

}
