from django.urls import path
from . import views

app_name = 'vss_handler'

urlpatterns = [
    path('', views.vss_detail, name='detail'),
    path('upload/', views.vss_upload, name='upload'),
]
