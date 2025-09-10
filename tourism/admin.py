from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Hotel, Destination, TravelOffer, OfferReservation, Payment,
    ClubService, SpecialOffer, Testimonial, Reservation, SearchQuery
)

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'address', 'is_active']
    list_filter = ['rating', 'is_active']
    search_fields = ['name', 'address']
    list_editable = ['is_active']

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'current_price', 'is_featured', 'created_at']
    list_filter = ['is_featured', 'package_type', 'departure_city']
    search_fields = ['name', 'location']
    list_editable = ['is_featured']
    filter_horizontal = ['hotels']
    fields = ['name', 'location', 'description', 'hotels', 'duration_days', 'duration_nights', 'package_type', 'departure_city', 'original_price', 'current_price', 'image', 'icon_class', 'is_featured']

@admin.register(TravelOffer)
class TravelOfferAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'get_destinations',  # Correction ici
        'departure_date',
        'offer_price',
        'max_participants',
        'available_spots_display',
        'is_active',
        'is_featured'
    ]
    list_filter = [
        'is_active',
        'is_featured',
        'departure_date'
    ]  # Retire 'offer_type' si le champ n'existe pas

    # Ajoute la méthode pour afficher les destinations
    def get_destinations(self, obj):
        return ", ".join([d.name for d in obj.destinations.all()])
    get_destinations.short_description = "Destinations"
    
    def available_spots_display(self, obj):
        return f"{obj.available_spots}/{obj.max_participants}"
    available_spots_display.short_description = "Places disponibles"
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('title', 'description', 'destinations', 'hotels', 'image')  # <-- AJOUT description
        }),
        ('Dates', {
            'fields': ('departure_date', 'return_date', 'booking_deadline')
        }),
        ('Prix et participants', {
            'fields': ('original_price', 'offer_price', 'max_participants', 'min_participants')
        }),
        ('Acompte', {
            'fields': ('deposit_percentage', 'deposit_amount'),
            'description': 'Configurez soit un pourcentage, soit un montant fixe d\'acompte'
        }),
        ('Services', {
            'fields': ('included_services', 'excluded_services', 'conditions'),
            'classes': ('collapse',)
        }),
        ('Statut', {
            'fields': ('is_active', 'is_featured')
        })
    )

@admin.register(OfferReservation)
class OfferReservationAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'offer', 'participants_count', 'total_price', 'deposit_amount', 'status', 'created_at'
]
    list_filter = ['status', 'payment_type', 'created_at']
    search_fields = ['client_name', 'client_email', 'offer__title']
    readonly_fields = ['total_price', 'deposit_amount', 'remaining_amount']
    
    fieldsets = (
        ('Réservation', {
            'fields': ('offer', 'participants_count', 'special_requests')
        }),
        ('Client', {
            'fields': ('client_name', 'client_email', 'client_phone')
        }),
        ('Paiement', {
            'fields': ('payment_type', 'total_price', 'deposit_amount', 'remaining_amount', 'status'),
            'classes': ('collapse',)
        }),
        ('Stripe', {
            'fields': ('stripe_payment_intent_id', 'stripe_customer_id', 'payment_status', 'paid_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['get_client_name', 'amount', 'status', 'is_deposit', 'get_reservation_info', 'created_at']
    list_filter = ['status', 'is_deposit', 'currency', 'created_at']
    search_fields = ['stripe_payment_intent_id', 'offer_reservation__client_name', 'reservation__client_name']
    readonly_fields = ['stripe_payment_intent_id', 'stripe_client_secret', 'created_at', 'updated_at']
    
    def get_client_name(self, obj):
        if obj.offer_reservation:
            return obj.offer_reservation.client_name
        elif obj.reservation:
            return obj.reservation.client_name
        return "N/A"
    get_client_name.short_description = "Client"
    
    def get_reservation_info(self, obj):
        if obj.offer_reservation:
            return format_html(
                '<strong>{}</strong><br><small>{} participants</small>',
                obj.offer_reservation.offer.title,
                obj.offer_reservation.participants_count
            )
        elif obj.reservation:
            return format_html(
                '<strong>{}</strong><br><small>{} voyageurs</small>',
                obj.reservation.destination.name,
                obj.reservation.travelers_count
            )
        return "N/A"
    get_reservation_info.short_description = "Réservation"
    
    fieldsets = (
        ('Paiement', {
            'fields': ('amount', 'currency', 'status', 'is_deposit')
        }),
        ('Réservations liées', {
            'fields': ('offer_reservation', 'reservation'),
            'description': 'Une seule des deux doit être remplie'
        }),
        ('Stripe', {
            'fields': ('stripe_payment_intent_id', 'stripe_client_secret', 'payment_method_id'),
            'classes': ('collapse',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(ClubService)
class ClubServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    ordering = ['order']

@admin.register(SpecialOffer)
class SpecialOfferAdmin(admin.ModelAdmin):
    list_display = ['title', 'offer_type', 'badge_text', 'valid_until', 'is_active']
    list_filter = ['offer_type', 'is_active']
    list_editable = ['is_active']

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'client_city', 'rating', 'is_featured', 'created_at']
    list_filter = ['rating', 'is_featured']
    list_editable = ['is_featured']

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'destination', 'departure_date', 'travelers_count', 'status', 'created_at']
    list_filter = ['status', 'departure_date']
    search_fields = ['client_name', 'client_email', 'destination__name']

@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ['destination', 'departure_date', 'duration', 'travelers_count', 'created_at']
    list_filter = ['destination', 'duration']
    readonly_fields = ['created_at']
