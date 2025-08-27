from django.urls import path
from . import views

app_name = 'tourism'

urlpatterns = [
    # Pages principales
    path('', views.home_view, name='home'),
    path('destinations/', views.DestinationListView.as_view(), name='destinations'),
    path('destinations/<int:pk>/', views.DestinationDetailView.as_view(), name='destination_detail'),
    path('clubs/', views.clubs_view, name='clubs'),
    path('offers/', views.offers_view, name='offers'),
    path('api/search-destinations/', views.search_destinations_ajax, name='search_destinations_ajax'),
    
    # Offres de voyage avec dates fixes
    path('offres/', views.offers_list, name='offers_list'),
    path('offres/<int:offer_id>/', views.offer_detail, name='offer_detail'),
    path('offres/reservation/<int:reservation_id>/paiement/', views.offer_payment, name='offer_payment'),
    path('offres/reservation/<int:reservation_id>/succes/', views.offer_payment_success, name='offer_payment_success'),
    
    # Réservations classiques (destinations)
    path('destinations/<int:destination_id>/reserver/', views.destination_reservation, name='destination_reservation'),
    path('reservation/<int:reservation_id>/paiement/', views.reservation_payment, name='payment'),
    path('reservation/<int:reservation_id>/succes/', views.payment_success, name='payment_success'),
    
    # Webhook Stripe
    path('stripe/webhook/', views.stripe_webhook, name='stripe_webhook'),
    
    # Page de contact
    path('contact/', views.contact_view, name='contact'),
]
