from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from wkhtmltopdf.views import PDFTemplateView

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
  path('auction/new/',views.AuctionCreateView.as_view(),name="auction_new"),
  path('auction/<int:pk>/edit/',views.AuctionUpdateView.as_view(),name="auction_edit"),
  path('survey/new/',views.SurveyCreateView.as_view(),name="survey_new" ),
  path('survey/<int:pk>/edit/',views.SurveyUpdateView.as_view(),name="survey_edit" ),
  path('clicklist/new/',views.ClickListCreateView.as_view(),name="clicklist_new" ),
  path('clicklist/<int:pk>/edit/',views.ClickListUpdateView.as_view(),name="clicklist_edit"),
  path('objectbuild/new/',views.ObjectBuildCreateView.as_view(),name="objectbuild_new" ),
  path('objectbuild/<int:pk>/edit/',views.ObjectBuildUpdateView.as_view(),name="objectbuild_edit"),
  path('objectbuild/<int:pk>/delete/',views.ObjectBuildDeleteView.as_view(),name="objectbuild_delete"),
  path('scorea/<int:pk>/edit/',views.ScoreAUpdateView.as_view(),name="score_a_edit"),
  path('scoreb/<int:pk>/edit/',views.ScoreBUpdateView.as_view(),name="score_b_edit"),
  path('scorec/<int:pk>/edit/',views.ScoreCUpdateView.as_view(),name="score_c_edit"),
  path('scorea/<int:pk>/delete/',views.ScoreADeleteView.as_view(),name="score_a_delete"),
  path('scoreb/<int:pk>/delete/',views.ScoreBDeleteView.as_view(),name="score_b_delete"),
  path('scorec/<int:pk>/delete/',views.ScoreCDeleteView.as_view(),name="score_c_delete"),
  path('regionalhead/new/',views.RegionalHeadCreateView.as_view(),name="regionalhead_new" ),
  path('regionalhead/<int:pk>/edit/',views.RegionalHeadUpdateView.as_view(),name="regionalhead_edit" ),
  path('regionalhead/<int:pk>/delete/',views.RegionalHeadDeleteView.as_view(),name="regionalhead_delete" ),
  path('subsigntruea/new/',views.SubSigntrueACreateView.as_view(),name="subsigntruea_new" ),
  path('subsigntruea/<int:pk>/edit/',views.SubSigntrueAUpdateView.as_view(),name="subsigntruea_edit" ),
  path('subsigntruea/<int:pk>/delete/',views.SubSigntrueADeleteView.as_view(),name="subsigntruea_delete" ),
  path('subsigntrueb/new/',views.SubSigntrueBCreateView.as_view(),name="subsigntrueb_new" ),
  path('subsigntrueb/<int:pk>/edit/',views.SubSigntrueBUpdateView.as_view(),name="subsigntrueb_edit" ),
  path('subsigntrueb/<int:pk>/delete/',views.SubSigntrueBDeleteView.as_view(),name="subsigntrueb_delete" ),
  path('ajax/load-townships/', views.load_townships, name='ajax_load_townships'),
  
  path('deedtax/<int:pk>/edit/', views.DeedtaxUpdateView.as_view(), name='deedtax_edit'),
  path('realestateregistration/<int:pk>/edit/', views.RealestateregistrationUpdateView.as_view(), name='realestateregistration_edit'),
  path('complaint/<int:pk>/edit/', views.ComplaintUpdateView.as_view(), name='complaint_edit'),
  path('letter/<int:pk>/edit/', views.LetterUpdateView.as_view(), name='letter_edit'),
  path('commonpropertydivision/<int:pk>/edit/', views.CommonpropertydivisionUpdateView.as_view(), name='commonpropertydivision_edit'),
  
  path('yfratingscalePDFView/<int:pk>/', views.yfratingscalePDFView.as_view(),name="yfratingscalePDF_View"),
  path('deedtaxPDFView/<int:pk>/', views.deedtaxPDFView.as_view(),name="deedtaxPDF_View"),
  path('realestateregistrationPDFView/<int:pk>/', views.realestateregistrationPDFView.as_view(),name="realestateregistrationPDF_View"),
  path('complaintPDFView/<int:pk>/', views.complaintPDFView.as_view(),name="complaintPDF_View"),
  path('letterPDFView/<int:pk>/', views.letterPDFView.as_view(),name="letterPDF_View"),
  path('commonpropertydivisionPDFView/<int:pk>/', views.commonpropertydivisionPDFView.as_view(),name="commonpropertydivisionPDF_View"),
]
