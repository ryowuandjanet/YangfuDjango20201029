from django.urls import path
from . import views

# app_name='yfcases'

urlpatterns = [
  path('', views.HomePageView.as_view(), name='home'),
]
