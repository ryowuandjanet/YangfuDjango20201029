from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name='yfcase'

urlpatterns = [
  path('login/',auth_views.LoginView.as_view(template_name='registration/login.html'),name='login'),
  path('',views.YfcaseListView.as_view(),name="home" ),
  path('yfcase/<int:pk>/',views.YfcaseDetailView.as_view(),name="yfcase_detail"),
  path('yfcase/new/',views.YfcaseCreateView.as_view(),name="yfcase_new"),
  path('yfcase/<int:pk>/edit/',views.YfcaseUpdateView.as_view(),name="yfcase_edit"),
  path('yfcase/<int:pk>/delete/',views.YfcaseDeleteView.as_view(),name="yfcase_delete"),
  path('land/new/',views.LandCreateView.as_view(),name="land_new"),
  path('land/<int:pk>/edit/',views.LandUpdateView.as_view(),name="land_edit"),
  path('land/<int:pk>/delete/',views.LandDeleteView.as_view(),name="land_delete"),
  path('build/new/',views.BuildCreateView.as_view(),name="build_new"),
  path('build/<int:pk>/edit/',views.BuildUpdateView.as_view(),name="build_edit"),
  path('build/<int:pk>/delete/',views.BuildDeleteView.as_view(),name="build_delete"),
  path('ajax/load-townships/', views.load_townships, name='ajax_load_townships'),
]
