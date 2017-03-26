from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt
from UserManagement import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]

urlpatterns+=[
    url(r'^sesion/$', views.sesion, name='sesion'),
]

urlpatterns+=[
    url(r'^register/$', views.register, name='register'),
]

urlpatterns+=[
    url(r'^register/$', views.register, name='register'),
]

urlpatterns+=[
    url(r'^login/$', views.user_login, name='login'),
]

urlpatterns+=[
    url(r'^logout/$', views.user_logout, name='logout'),
]

urlpatterns+=[
    url(r'^logout/$', views.user_logout, name='logout'),
]
