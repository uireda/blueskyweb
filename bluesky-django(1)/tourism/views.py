from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
from .models import Destination, ClubService, SpecialOffer, Testimonial
from .forms import SearchForm, ContactForm
import json

def home_view(request):
    """Vue principale de la page d'accueil"""
    # Récupérer les données pour la page d'accueil
    featured_destinations = Destination.objects.filter(is_featured=True)[:6]
    club_services = ClubService.objects.filter(is_active=True)[:6]
    special_offers = SpecialOffer.objects.filter(is_active=True)[:3]
    testimonials = Testimonial.objects.filter(is_featured=True)[:3]
    
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

def clubs_view(request):
    """Vue pour la page des clubs"""
    club_services = ClubService.objects.filter(is_active=True)
    return render(request, 'tourism/clubs.html', {'club_services': club_services})

def offers_view(request):
    """Vue pour la page des offres spéciales"""
    special_offers = SpecialOffer.objects.filter(is_active=True)
    return render(request, 'tourism/offers.html', {'special_offers': special_offers})
