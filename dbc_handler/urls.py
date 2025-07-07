from django.urls import path
from . import views

app_name = 'dbc_handler'

urlpatterns = [
    path('', views.dbc_detail, name='detail'),
    path('upload/', views.upload_dbc, name='upload'),
]
