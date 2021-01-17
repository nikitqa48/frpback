from django.urls import path
from .views import *

urlpatterns = [
    path('branch/', BranchView.as_view()),
    # path('branch/<slug:slug>/', DetailBranchView.as_view()),
    path('branch/company/<slug:slug>/', CompanyView.as_view()),
    path('branch/company/detail/<slug:slug>', DetailCompanyView.as_view()),
    path('branch/product/<slug:company>/', ProductCompanyView.as_view()),
    path('product/<slug:name>/', ProductDetailView.as_view())
]