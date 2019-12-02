from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path('u/', views.model_form_upload,name='model_form_upload'),
]