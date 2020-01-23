from accounts import views
from django.conf.urls import url

app_name = 'accounts'

urlpatterns=[
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    url(r'^already_logged/',views.already_logged,name='already_logged'),
    url(r'^logout/$', views.user_logout, name='logout'),
]