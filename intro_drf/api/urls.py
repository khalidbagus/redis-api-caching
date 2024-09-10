from .views import *
from django.urls import path, include

urlpatterns = [
    path('get-institution-trade', InstitutionsView.as_view(), name='get-institution-trade'),
    path('get-reports', ReportsView.as_view(), name='get-reports'),
    path('get-metadata', MetadataView.as_view(), name='get-metadata')
]
