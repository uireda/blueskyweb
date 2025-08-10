from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from .models import (
    Destination, ClubService, SpecialOffer, Testimonial, 
    TravelOffer, OfferReservation, Payment, Reservation, SearchQuery
)
from .forms import SearchForm, ContactForm, OfferReservationForm
import stripe
import json

# Configuration Stripe
stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', '')

def home_view(request):
    """Vue principale de la page d'accueil"""
    # Récupérer les données pour la page d'accueil
    featured_destinations = Destination.objects.filter(is_featured=True)[:6]
    club_services = ClubService.objects.filter(is_active=True)[:6]
    special_offers = SpecialOffer.objects.filter(is_active=True)[:3]
    testimonials = Testimonial.objects.filter(is_featured=True)[:3]
    featured_travel_offers = TravelOffer.objects.filter(is_featured=True, is_active=True)[:3]
    
    # Formulaire de recherche
    search_form = SearchForm()
    
    # Traitement du formulaire de recherche
    if request.method == 'POST' and 'search_submit' in request.POST:
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            search_query = search_form.save()
            messages.success(request, 'Votre recherche a été enregistrée. Nous vous contacterons bientôt avec les meilleures offres!')
            return redirect('tourism:home')
    
    # Formulaire de contact
    contact_form = ContactForm()
    if request.method == 'POST' and 'contact_submit' in request.POST:
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            # Envoyer l'email de contact
            try:
                send_mail(
                    subject=f"Contact BlueSky: {contact_form.cleaned_data['subject']}",
                    message=f"""
                    Nouveau message de contact:
                    
                    Nom: {contact_form.cleaned_data['name']}
                    Email: {contact_form.cleaned_data['email']}
                    Téléphone: {contact_form.cleaned_data['phone']}
                    
                    Message:
                    {contact_form.cleaned_data['message']}
                    """,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['bluesky13001@gmail.com'],
                    fail_silently=False,
                )
                messages.success(request, 'Votre message a été envoyé avec succès!')
                return redirect('tourism:home')
            except Exception as e:
                messages.error(request, 'Erreur lors de l\'envoi du message. Veuillez réessayer.')
    
    context = {
        'destinations': featured_destinations,
        'club_services': club_services,
        'special_offers': special_offers,
        'testimonials': testimonials,
        'featured_travel_offers': featured_travel_offers,
        'search_form': search_form,
        'contact_form': contact_form,
    }
    
    return render(request, 'tourism/home.html', context)

class DestinationListView(ListView):
    """Vue pour lister toutes les destinations"""
    model = Destination
    template_name = 'tourism/destinations.html'
    context_object_name = 'destinations'
    paginate_by = 12

    def get_queryset(self):
        queryset = Destination.objects.all()
        
        # Filtrage par destination
        destination_filter = self.request.GET.get('destination')
        if destination_filter:
            queryset = queryset.filter(location__icontains=destination_filter)
        
        # Filtrage par prix
        max_price = self.request.GET.get('max_price')
        if max_price:
            try:
                queryset = queryset.filter(current_price__lte=float(max_price))
            except ValueError:
                pass
        
        return queryset

class DestinationDetailView(DetailView):
    """Vue pour les détails d'une destination"""
    model = Destination
    template_name = 'tourism/destination_detail.html'
    context_object_name = 'destination'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ajouter un formulaire de réservation vide pour l'affichage
        context['reservation_form'] = None  # Sera implémenté plus tard
        return context

def clubs_view(request):
    """Vue pour la page des clubs"""
    club_services = ClubService.objects.filter(is_active=True)
    return render(request, 'tourism/clubs.html', {'club_services': club_services})

def offers_view(request):
    """Vue pour la page des offres spéciales"""
    special_offers = SpecialOffer.objects.filter(is_active=True)
    return render(request, 'tourism/offers.html', {'special_offers': special_offers})

@csrf_exempt
def search_destinations_ajax(request):
    """Vue AJAX pour la recherche de destinations"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            destination = data.get('destination', '')
            max_price = data.get('max_price', '')
            
            queryset = Destination.objects.all()
            
            if destination:
                queryset = queryset.filter(location__icontains=destination)
            
            if max_price:
                queryset = queryset.filter(current_price__lte=float(max_price))
            
            results = []
            for dest in queryset[:10]:  # Limiter à 10 résultats
                results.append({
                    'id': dest.id,
                    'name': dest.name,
                    'location': dest.location,
                    'current_price': float(dest.current_price),
                    'original_price': float(dest.original_price),
                    'hotel_rating': dest.hotel_rating_display,
                    'duration_days': dest.duration_days,
                    'duration_nights': dest.duration_nights,
                })
            
            return JsonResponse({'results': results})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# ===== VUES POUR LES OFFRES DE VOYAGE =====

def offers_list(request):
    """Liste des offres de voyage"""
    offers = TravelOffer.objects.filter(is_active=True).order_by('-is_featured', 'departure_date')
    
    # Filtres
    offer_type = request.GET.get('type')
    if offer_type:
        offers = offers.filter(offer_type=offer_type)
    
    context = {
        'offers': offers,
        'offer_types': TravelOffer.OFFER_TYPES,
        'selected_type': offer_type,
    }
    return render(request, 'tourism/offers_list.html', context)

def offer_detail(request, offer_id):
    """Détail d'une offre avec formulaire de réservation"""
    offer = get_object_or_404(TravelOffer, id=offer_id, is_active=True)
    
    if request.method == 'POST':
        form = OfferReservationForm(request.POST, offer=offer)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.offer = offer
            reservation.save()
            
            # Rediriger vers la page de paiement
            return redirect('tourism:offer_payment', reservation_id=reservation.id)
    else:
        form = OfferReservationForm(offer=offer)
    
    context = {
        'offer': offer,
        'form': form,
    }
    return render(request, 'tourism/offer_detail.html', context)

def offer_payment(request, reservation_id):
    """Page de paiement pour une réservation d'offre"""
    reservation = get_object_or_404(OfferReservation, id=reservation_id)
    
    if not stripe.api_key:
        messages.error(request, "Le système de paiement n'est pas configuré.")
        return redirect('tourism:offer_detail', offer_id=reservation.offer.id)
    
    try:
        # Créer un PaymentIntent Stripe
        intent = stripe.PaymentIntent.create(
            amount=reservation.amount_to_pay_cents,
            currency='eur',
            metadata={
                'reservation_id': reservation.id,
                'offer_title': reservation.offer.title,
                'client_name': reservation.client_name,
                'payment_type': reservation.payment_type,
            }
        )
        
        # Sauvegarder l'ID du PaymentIntent
        reservation.stripe_payment_intent_id = intent.id
        reservation.save()
        
        # Créer un enregistrement de paiement
        payment = Payment.objects.create(
            offer_reservation=reservation,
            stripe_payment_intent_id=intent.id,
            amount=reservation.amount_to_pay,
            stripe_client_secret=intent.client_secret,
            is_deposit=(reservation.payment_type == 'deposit'),
            status='pending'
        )
        
        context = {
            'reservation': reservation,
            'payment': payment,
            'stripe_public_key': getattr(settings, 'STRIPE_PUBLISHABLE_KEY', ''),
            'client_secret': intent.client_secret,
        }
        return render(request, 'tourism/offer_payment.html', context)
        
    except stripe.error.StripeError as e:
        messages.error(request, f"Erreur de paiement: {str(e)}")
        return redirect('tourism:offer_detail', offer_id=reservation.offer.id)

def offer_payment_success(request, reservation_id):
    """Page de confirmation de paiement"""
    reservation = get_object_or_404(OfferReservation, id=reservation_id)
    
    context = {
        'reservation': reservation,
    }
    return render(request, 'tourism/offer_payment_success.html', context)

# ===== VUES POUR LES RÉSERVATIONS CLASSIQUES =====

def destination_reservation(request, destination_id):
    """Vue pour réserver une destination classique"""
    destination = get_object_or_404(Destination, id=destination_id)
    
    # Cette vue sera implémentée plus tard
    messages.info(request, "La réservation en ligne sera bientôt disponible. Contactez-nous par téléphone.")
    return redirect('tourism:destination_detail', pk=destination_id)

def reservation_payment(request, reservation_id):
    """Page de paiement pour une réservation classique"""
    reservation = get_object_or_404(Reservation, id=reservation_id)
    
    # Cette vue sera implémentée plus tard
    messages.info(request, "Le paiement en ligne sera bientôt disponible.")
    return redirect('tourism:home')

def payment_success(request, reservation_id):
    """Page de confirmation de paiement pour réservation classique"""
    reservation = get_object_or_404(Reservation, id=reservation_id)
    
    context = {
        'reservation': reservation,
    }
    return render(request, 'tourism/payment_success.html', context)

# ===== WEBHOOK STRIPE =====

@csrf_exempt
@require_POST
def stripe_webhook(request):
    """Webhook pour traiter les événements Stripe"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', '')

    if not endpoint_secret:
        return JsonResponse({'error': 'Webhook secret not configured'}, status=400)

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    # Traiter l'événement
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        
        try:
            # Trouver la réservation correspondante
            reservation = OfferReservation.objects.get(
                stripe_payment_intent_id=payment_intent['id']
            )
            
            # Mettre à jour le statut
            if reservation.payment_type == 'full':
                reservation.status = 'paid'
            else:
                reservation.status = 'deposit_paid'
            
            reservation.payment_status = 'succeeded'
            reservation.save()
            
            # Mettre à jour le paiement
            payment = Payment.objects.get(
                stripe_payment_intent_id=payment_intent['id']
            )
            payment.status = 'succeeded'
            payment.save()
            
            # Réduire les places disponibles (cette logique sera corrigée dans le modèle)
            # reservation.offer.available_spots -= reservation.participants_count
            # reservation.offer.save()
            
        except (OfferReservation.DoesNotExist, Payment.DoesNotExist):
            pass
    
    return JsonResponse({'status': 'success'})
