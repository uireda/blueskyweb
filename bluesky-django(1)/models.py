from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Destination(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nom de la destination")
    location = models.CharField(max_length=200, verbose_name="Lieu")
    hotel_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Étoiles de l'hôtel"
    )
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
        return f"{self.name} - {self.location}"

    @property
    def discount_percentage(self):
        if self.original_price > self.current_price:
            return round(((self.original_price - self.current_price) / self.original_price) * 100)
        return 0

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
