from django.urls import path
from . import views

app_name = 'mapping'

urlpatterns = [
    path('', views.vss_dbc_mapping_detail, name='detail'),
    path('create/', views.vss_dbc_mapping_create, name='create'),
]
