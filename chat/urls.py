from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/$',views.home,name='home'),
    url(r'login/$',views.login, name='login'),
	url(r'auth/$',views.auth_view),
	url(r'logout/$',views.logout,name='logout'),
	url(r'invalid/$',views.invalid_login,name='invalid_login'),
	url(r'register/$',views.register_user, name='register'),
	url(r'register_success/$',views.register_success,name='register_success'),
	url(r'chat_window/(?P<pk>\d+)$',views.chat_window,name='chat_window'),
    ]