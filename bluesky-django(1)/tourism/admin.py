from django.contrib import admin
from .models import Destination, ClubService, SpecialOffer, Testimonial, SearchQuery, Hotel, Reservation

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'address', 'phone', 'is_active', 'created_at']
    list_filter = ['rating', 'is_active', 'created_at']
    search_fields = ['name', 'address', 'phone', 'email']
    list_editable = ['is_active']
    ordering = ['name']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('name', 'rating', 'description')
        }),
        ('Contact', {
            'fields': ('address', 'phone', 'email', 'website')
        }),
        ('Équipements et médias', {
            'fields': ('amenities', 'image')
        }),
        ('Statut', {
            'fields': ('is_active',)
        }),
    )

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'get_hotels', 'current_price', 'original_price', 'is_featured', 'created_at']
    list_filter = ['is_featured', 'departure_city', 'created_at', 'hotels']
    search_fields = ['name', 'location', 'departure_city', 'hotels__name']
    list_editable = ['is_featured', 'current_price']
    ordering = ['-created_at']
    filter_horizontal = ['hotels']  # Interface pour sélectionner plusieurs hôtels
    
    def get_hotels(self, obj):
        return ", ".join([f"{hotel.name} ({hotel.rating}*)" for hotel in obj.hotels.all()[:3]])
    get_hotels.short_description = 'Hôtels'
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('name', 'location', 'hotels', 'package_type', 'departure_city')
        }),
        ('Durée et prix', {
            'fields': ('duration_days', 'duration_nights', 'original_price', 'current_price')
        }),
        ('Affichage', {
            'fields': ('image', 'icon_class', 'is_featured')
        }),
    )

@admin.register(ClubService)
class ClubServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['title', 'description']
    list_editable = ['is_active', 'order']
    ordering = ['order']

@admin.register(SpecialOffer)
class SpecialOfferAdmin(admin.ModelAdmin):
    list_display = ['title', 'offer_type', 'badge_text', 'valid_until', 'is_active', 'created_at']
    list_filter = ['offer_type', 'is_active', 'valid_until']
    search_fields = ['title', 'description']
    list_editable = ['is_active']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Informations de l\'offre', {
            'fields': ('title', 'offer_type', 'badge_text')
        }),
        ('Contenu', {
            'fields': ('description', 'conditions')
        }),
        ('Validité', {
            'fields': ('valid_until', 'is_active')
        }),
    )

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'client_city', 'rating', 'is_featured', 'created_at']
    list_filter = ['rating', 'is_featured', 'created_at']
    search_fields = ['client_name', 'client_city', 'comment']
    list_editable = ['is_featured']
    ordering = ['-created_at']

@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ['destination', 'departure_date', 'duration', 'travelers_count', 'email', 'created_at']
    list_filter = ['destination', 'duration', 'departure_date']
    search_fields = ['email', 'phone']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    def has_add_permission(self, request):
        return False  # Empêcher l'ajout manuel depuis l'admin

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'destination', 'departure_date', 'travelers_count', 'status', 'total_estimated_price', 'created_at']
    list_filter = ['status', 'departure_date', 'destination', 'created_at']
    search_fields = ['client_name', 'client_email', 'client_phone', 'destination__name']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at', 'estimated_total']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Informations client', {
            'fields': ('client_name', 'client_email', 'client_phone')
        }),
        ('Détails du voyage', {
            'fields': ('destination', 'departure_date', 'travelers_count', 'hotel_preference')
        }),
        ('Demandes et prix', {
            'fields': ('special_requests', 'total_estimated_price', 'estimated_total')
        }),
        ('Statut et dates', {
            'fields': ('status', 'created_at', 'updated_at')
        }),
    )

    def save_model(self, request, obj, form, change):
        # Calculer le prix estimé automatiquement
        if obj.destination and obj.travelers_count:
            obj.total_estimated_price = obj.destination.current_price * obj.travelers_count
        super().save_model(request, obj, form, change)
