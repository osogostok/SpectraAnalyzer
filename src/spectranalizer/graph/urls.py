from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    # re_path(r'^graph_name/(?P<spectr_name>[\w-]+)/$', graph_spectr),
    path('graph/', graph_spectr, name='graph') ,
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register')
    
]
