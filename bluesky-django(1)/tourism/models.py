from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class Hotel(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nom de l'hôtel")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Étoiles de l'hôtel"
    )
    description = models.TextField(verbose_name="Description de l'hôtel", blank=True)
    amenities = models.TextField(verbose_name="Équipements", blank=True, help_text="Séparez les équipements par des virgules")
    image = models.ImageField(upload_to='hotels/', blank=True, null=True, verbose_name="Image de l'hôtel")
    address = models.CharField(max_length=300, verbose_name="Adresse", blank=True)
    phone = models.CharField(max_length=20, verbose_name="Téléphone", blank=True)
    email = models.EmailField(verbose_name="Email", blank=True)
    website = models.URLField(verbose_name="Site web", blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hôtel"
        verbose_name_plural = "Hôtels"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.rating}*)"

    @property
    def amenities_list(self):
        if self.amenities:
            return [amenity.strip() for amenity in self.amenities.split(',')]
        return []

class Destination(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nom de la destination")
    location = models.CharField(max_length=200, verbose_name="Lieu")
    description = models.TextField(verbose_name="Description", blank=True)  # <-- AJOUT ICI
    hotels = models.ManyToManyField('Hotel', verbose_name="Hôtels", related_name="destinations", blank=True)
    duration_days = models.IntegerField(verbose_name="Durée en jours")
    duration_nights = models.IntegerField(verbose_name="Durée en nuits")
    package_type = models.CharField(max_length=100, default="Tout inclus")
    departure_city = models.CharField(max_length=100, verbose_name="Ville de départ")
    original_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix original")
    current_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix actuel")
    image = models.ImageField(upload_to='destinations/', blank=True, null=True)
    icon_class = models.CharField(max_length=100, default="fas fa-umbrella-beach")
    is_featured = models.BooleanField(default=False, verbose_name="Destination phare")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Destination"
        verbose_name_plural = "Destinations"
        ordering = ['-created_at']

    def __str__(self):
        hotels_list = ", ".join([hotel.name for hotel in self.hotels.all()[:2]])
        if self.hotels.count() > 2:
            hotels_list += f" (+{self.hotels.count() - 2} autres)"
        return f"{self.name} - {self.location} ({hotels_list})"

    @property
    def discount_percentage(self):
        if self.original_price > self.current_price:
            return round(((self.original_price - self.current_price) / self.original_price) * 100)
        return 0

    @property
    def hotel_rating_display(self):
        """Affiche les étoiles des hôtels pour l'affichage"""
        ratings = list(set([hotel.rating for hotel in self.hotels.all()]))
        if len(ratings) == 1:
            return f"{ratings[0]}*"
        elif len(ratings) > 1:
            return f"{min(ratings)}-{max(ratings)}*"
        return "N/A"

    @property
    def hotels_list(self):
        """Retourne la liste des hôtels avec leurs étoiles"""
        return [(hotel.name, hotel.rating) for hotel in self.hotels.all()]

class TravelOffer(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(verbose_name="Description", blank=True)  # <-- AJOUT ICI
    destinations = models.ManyToManyField('Destination', related_name='offers', verbose_name="Destinations")
    hotels = models.ManyToManyField('Hotel', related_name='offers', verbose_name="Hôtels")
    departure_date = models.DateField(verbose_name="Date de départ")
    return_date = models.DateField(verbose_name="Date de retour")
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix par personne")
    
    # Prix et capacité
    original_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix original par personne")
    min_participants = models.IntegerField(default=1, verbose_name="Nombre minimum de participants")
    max_participants = models.IntegerField(verbose_name="Nombre maximum de participants")
    
    # Acompte
    deposit_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=Decimal('30.00'),
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Pourcentage d'acompte (%)"
    )
    deposit_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="Montant d'acompte fixe (optionnel)"
    )
    
    # Informations supplémentaires
    included_services = models.TextField(verbose_name="Services inclus", blank=True)
    excluded_services = models.TextField(verbose_name="Services non inclus", blank=True)
    conditions = models.TextField(verbose_name="Conditions particulières", blank=True)
    
    # Statut et visibilité
    is_active = models.BooleanField(default=True, verbose_name="Offre active")
    is_featured = models.BooleanField(default=False, verbose_name="Offre vedette")
    booking_deadline = models.DateField(verbose_name="Date limite de réservation", null=True, blank=True)
    
    # Images
    image = models.ImageField(upload_to='offers/', blank=True, null=True, verbose_name="Image de l'offre")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Offre de Voyage"
        verbose_name_plural = "Offres de Voyage"
        ordering = ['departure_date', '-created_at']

    def __str__(self):
        return f"{self.title} - {self.departure_date}"

    @property
    def discount_percentage(self):
        if self.original_price > self.offer_price:
            return round(((self.original_price - self.offer_price) / self.original_price) * 100)
        return 0

    @property
    def duration_days(self):
        return (self.return_date - self.departure_date).days + 1

    @property
    def duration_nights(self):
        return (self.return_date - self.departure_date).days

    @property
    def available_spots(self):
        """Nombre de places disponibles"""
        booked = OfferReservation.objects.filter(
            offer=self, 
            status__in=['confirmed', 'paid', 'deposit_paid']
        ).aggregate(
            total=models.Sum('participants_count')
        )['total'] or 0
        return self.max_participants - booked

    @property
    def is_available(self):
        """Vérifie si l'offre est encore disponible"""
        return self.is_active and self.available_spots > 0

    def get_deposit_amount(self, total_price):
        """Calcule le montant de l'acompte"""
        if self.deposit_amount:
            return self.deposit_amount
        return (total_price * self.deposit_percentage) / 100

    @property
    def calculated_deposit_amount(self):
        """Calcule et retourne le montant de l'acompte pour cette offre"""
        if self.deposit_amount:
            return self.deposit_amount
        return (self.offer_price * self.deposit_percentage) / 100

    @property
    def included_services_list(self):
        if self.included_services:
            return [service.strip() for service in self.included_services.split('\n') if service.strip()]
        return []

    @property
    def excluded_services_list(self):
        if self.excluded_services:
            return [service.strip() for service in self.excluded_services.split('\n') if service.strip()]
        return []

class ClubService(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre du service")
    description = models.TextField(verbose_name="Description")
    icon_class = models.CharField(max_length=100, verbose_name="Classe d'icône")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    order = models.IntegerField(default=0, verbose_name="Ordre d'affichage")

    class Meta:
        verbose_name = "Service Club"
        verbose_name_plural = "Services Club"
        ordering = ['order']

    def __str__(self):
        return self.title

class SpecialOffer(models.Model):
    OFFER_TYPES = [
        ('discount', 'Réduction'),
        ('free_child', 'Enfant Gratuit'),
        ('last_minute', 'Dernière Minute'),
        ('early_booking', 'Réservation Anticipée'),
    ]

    title = models.CharField(max_length=200, verbose_name="Titre de l'offre")
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPES, verbose_name="Type d'offre")
    badge_text = models.CharField(max_length=100, verbose_name="Texte du badge")
    description = models.TextField(verbose_name="Description")
    conditions = models.TextField(verbose_name="Conditions", blank=True)
    valid_until = models.DateField(verbose_name="Valable jusqu'au", blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Offre Spéciale"
        verbose_name_plural = "Offres Spéciales"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Testimonial(models.Model):
    client_name = models.CharField(max_length=200, verbose_name="Nom du client")
    client_city = models.CharField(max_length=100, verbose_name="Ville du client")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5,
        verbose_name="Note"
    )
    comment = models.TextField(verbose_name="Commentaire")
    is_featured = models.BooleanField(default=False, verbose_name="Témoignage vedette")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Témoignage"
        verbose_name_plural = "Témoignages"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.client_name} - {self.client_city}"

    @property
    def stars_range(self):
        return range(self.rating)

class Reservation(models.Model):
    RESERVATION_STATUS = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmée'),
        ('paid', 'Payée'),
        ('cancelled', 'Annulée'),
    ]

    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, verbose_name="Destination")
    client_name = models.CharField(max_length=200, verbose_name="Nom complet")
    client_email = models.EmailField(verbose_name="Email")
    client_phone = models.CharField(max_length=20, verbose_name="Téléphone")
    departure_date = models.DateField(verbose_name="Date de départ souhaitée")
    travelers_count = models.IntegerField(verbose_name="Nombre de voyageurs")
    hotel_preference = models.CharField(max_length=200, blank=True, verbose_name="Préférence d'hôtel")
    special_requests = models.TextField(blank=True, verbose_name="Demandes spéciales")
    status = models.CharField(max_length=20, choices=RESERVATION_STATUS, default='pending', verbose_name="Statut")
    total_estimated_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Prix estimé total")
    
    # Champs pour le paiement Stripe
    stripe_payment_intent_id = models.CharField(max_length=200, blank=True, null=True, verbose_name="ID Stripe Payment Intent")
    stripe_customer_id = models.CharField(max_length=200, blank=True, null=True, verbose_name="ID Client Stripe")
    payment_status = models.CharField(max_length=50, blank=True, verbose_name="Statut du paiement")
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name="Date de paiement")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Réservation"
        verbose_name_plural = "Réservations"
        ordering = ['-created_at']

    def __str__(self):
        return f"Réservation {self.client_name} - {self.destination.name} ({self.get_status_display()})"

    @property
    def estimated_total(self):
        if self.destination:
            return self.destination.current_price * self.travelers_count
        return 0

    @property
    def total_price_cents(self):
        """Prix total en centimes pour Stripe"""
        return int(self.estimated_total * 100)

class OfferReservation(models.Model):
    """Réservations pour les offres de voyage"""
    RESERVATION_STATUS = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmée'),
        ('deposit_paid', 'Acompte payé'),
        ('paid', 'Payée intégralement'),
        ('cancelled', 'Annulée'),
    ]

    PAYMENT_TYPE = [
        ('full', 'Paiement intégral'),
        ('deposit', 'Acompte seulement'),
    ]

    offer = models.ForeignKey(TravelOffer, on_delete=models.CASCADE, verbose_name="Offre", related_name="reservations")
    client_name = models.CharField(max_length=200, verbose_name="Nom complet")
    client_email = models.EmailField(verbose_name="Email")
    client_phone = models.CharField(max_length=20, verbose_name="Téléphone")
    participants_count = models.IntegerField(verbose_name="Nombre de participants")
    special_requests = models.TextField(blank=True, verbose_name="Demandes spéciales")
    
    # Prix et paiement
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix total")
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant de l'acompte")
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant restant")
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPE, default='deposit', verbose_name="Type de paiement")
    
    # Statut
    status = models.CharField(max_length=20, choices=RESERVATION_STATUS, default='pending', verbose_name="Statut")
    
    # Champs pour le paiement Stripe
    stripe_payment_intent_id = models.CharField(max_length=200, blank=True, null=True, verbose_name="ID Stripe Payment Intent")
    stripe_customer_id = models.CharField(max_length=200, blank=True, null=True, verbose_name="ID Client Stripe")
    payment_status = models.CharField(max_length=50, blank=True, verbose_name="Statut du paiement")
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name="Date de paiement")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Réservation d'Offre"
        verbose_name_plural = "Réservations d'Offres"
        ordering = ['-created_at']

    def __str__(self):
        return f"Réservation {self.client_name} - {self.offer.title} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        # Calculer automatiquement les montants
        if not self.total_price:
            self.total_price = self.offer.offer_price * self.participants_count
        
        if not self.deposit_amount:
            self.deposit_amount = self.offer.get_deposit_amount(self.total_price)
        
        if not self.remaining_amount:
            self.remaining_amount = self.total_price - self.deposit_amount
        
        super().save(*args, **kwargs)

    @property
    def amount_to_pay(self):
        """Montant à payer selon le type de paiement choisi"""
        if self.payment_type == 'full':
            return self.total_price
        return self.deposit_amount

    @property
    def amount_to_pay_cents(self):
        """Montant à payer en centimes pour Stripe"""
        return int(self.amount_to_pay * 100)

class Payment(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'En attente'),
        ('processing', 'En cours'),
        ('succeeded', 'Réussi'),
        ('failed', 'Échoué'),
        ('cancelled', 'Annulé'),
        ('refunded', 'Remboursé'),
    ]

    # Relations (une seule des deux doit être remplie)
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Réservation")
    offer_reservation = models.ForeignKey(OfferReservation, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Réservation d'offre", related_name="payments")
    
    stripe_payment_intent_id = models.CharField(max_length=200, unique=True, verbose_name="ID Stripe Payment Intent")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant")
    currency = models.CharField(max_length=3, default='EUR', verbose_name="Devise")
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending', verbose_name="Statut")
    stripe_client_secret = models.CharField(max_length=200, blank=True, verbose_name="Client Secret Stripe")
    payment_method_id = models.CharField(max_length=200, blank=True, verbose_name="ID Méthode de paiement")
    is_deposit = models.BooleanField(default=False, verbose_name="Est un acompte")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"
        ordering = ['-created_at']

    def __str__(self):
        client_name = ""
        if self.reservation:
            client_name = self.reservation.client_name
        elif self.offer_reservation:
            client_name = self.offer_reservation.client_name
        
        deposit_text = " (Acompte)" if self.is_deposit else ""
        return f"Paiement {self.amount}€{deposit_text} - {client_name} ({self.get_status_display()})"

class SearchQuery(models.Model):
    DESTINATIONS_CHOICES = [
        ('tunisie', 'Tunisie'),
        ('espagne', 'Espagne'),
        ('grece', 'Grèce'),
        ('turquie', 'Turquie'),
        ('maroc', 'Maroc'),
    ]

    DURATION_CHOICES = [
        ('3-4', '3-4 jours'),
        ('7', '1 semaine'),
        ('14', '2 semaines'),
        ('21', '3 semaines'),
    ]

    destination = models.CharField(max_length=50, choices=DESTINATIONS_CHOICES)
    departure_date = models.DateField(verbose_name="Date de départ")
    duration = models.CharField(max_length=10, choices=DURATION_CHOICES, verbose_name="Durée")
    travelers_count = models.IntegerField(verbose_name="Nombre de voyageurs")
    email = models.EmailField(blank=True, verbose_name="Email de contact")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Recherche"
        verbose_name_plural = "Recherches"
        ordering = ['-created_at'] 

    def __str__(self):
        return f"Recherche {self.destination} - {self.departure_date}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)