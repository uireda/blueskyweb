from django.contrib import admin
from .models import Destination, ClubService, SpecialOffer, Testimonial, SearchQuery

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'hotel_rating', 'current_price', 'original_price', 'is_featured', 'created_at']
    list_filter = ['hotel_rating', 'is_featured', 'departure_city', 'created_at']
    search_fields = ['name', 'location', 'departure_city']
    list_editable = ['is_featured', 'current_price']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('name', 'location', 'hotel_rating', 'package_type', 'departure_city')
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
