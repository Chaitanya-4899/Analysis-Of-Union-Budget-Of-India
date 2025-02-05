# analysis/urls.py

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_dataset, name='upload_dataset'),
    path('datasets/', views.view_datasets, name='view_datasets'),
    path('analysis/<int:dataset_id>/', views.view_analysis, name='view_analysis'),
    path('reports/', views.reports_dashboard, name='reports_dashboard'),
    path('sentiment/', views.sentiment_analysis, name='sentiment_analysis'),
]
