from django.urls import path
from . import views

app_name = 'tourism'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('destinations/', views.DestinationListView.as_view(), name='destinations'),
    path('destinations/<int:pk>/', views.DestinationDetailView.as_view(), name='destination_detail'),
    path('clubs/', views.clubs_view, name='clubs'),
    path('offers/', views.offers_view, name='offers'),
    path('api/search-destinations/', views.search_destinations_ajax, name='search_destinations_ajax'),
]
