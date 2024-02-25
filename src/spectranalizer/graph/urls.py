from django.urls import path, include
from .views import *
from spectranalizer import settings

urlpatterns = [
    path('', index, name='home'),
    path('graph/', GraphSpectrs.as_view(), name='graph'),

    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('update_spectr/', UpdateSpectrView.as_view(), name='update_spectr'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns


handler404 = pageNotFound
