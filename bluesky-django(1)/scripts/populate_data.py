import os
import django
from decimal import Decimal
from datetime import date, timedelta

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

from tourism.models import Destination, ClubService, SpecialOffer, Testimonial

def populate_destinations():
    """Peupler la base de données avec des destinations"""
    destinations_data = [
        {
            'name': 'Tunisie - Yasmine Hammamet',
            'location': 'Yasmine Hammamet',
            'hotel_rating': 4,
            'duration_days': 8,
            'duration_nights': 7,
            'package_type': 'Tout inclus',
            'departure_city': 'Paris',
            'original_price': Decimal('899.00'),
            'current_price': Decimal('751.00'),
            'icon_class': 'fas fa-umbrella-beach',
            'is_featured': True,
        },
        {
            'name': 'Baléares - Porto Cristo',
            'location': 'Porto Cristo',
            'hotel_rating': 4,
            'duration_days': 8,
            'duration_nights': 7,
            'package_type': 'Tout inclus',
            'departure_city': 'Lyon',
            'original_price': Decimal('1050.00'),
            'current_price': Decimal('776.00'),
            'icon_class': 'fas fa-umbrella-beach',
            'is_featured': True,
        },
        {
            'name': 'Canaries - Costa Adeje',
            'location': 'Costa Adeje',
            'hotel_rating': 4,
            'duration_days': 8,
            'duration_nights': 7,
            'package_type': 'Tout inclus',
            'departure_city': 'Marseille',
            'original_price': Decimal('1299.00'),
            'current_price': Decimal('1078.00'),
            'icon_class': 'fas fa-mountain',
            'is_featured': True,
        },
        {
            'name': 'Crète - Bali',
            'location': 'Bali, Crète',
            'hotel_rating': 3,
            'duration_days': 8,
            'duration_nights': 7,
            'package_type': 'Tout inclus',
            'departure_city': 'Nice',
            'original_price': Decimal('1020.00'),
            'current_price': Decimal('801.00'),
            'icon_class': 'fas fa-ship',
            'is_featured': True,
        },
        {
            'name': 'Djerba - Tunisie',
            'location': 'Djerba',
            'hotel_rating': 4,
            'duration_days': 8,
            'duration_nights': 7,
            'package_type': 'Tout inclus',
            'departure_city': 'Toulouse',
            'original_price': Decimal('850.00'),
            'current_price': Decimal('679.00'),
            'icon_class': 'fas fa-palm-tree',
            'is_featured': True,
        },
        {
            'name': 'Grèce - Vravrona',
            'location': 'Vravrona',
            'hotel_rating': 5,
            'duration_days': 8,
            'duration_nights': 7,
            'package_type': 'Tout inclus',
            'departure_city': 'Bordeaux',
            'original_price': Decimal('1100.00'),
            'current_price': Decimal('821.00'),
            'icon_class': 'fas fa-building',
            'is_featured': True,
        },
    ]

    for dest_data in destinations_data:
        destination, created = Destination.objects.get_or_create(
            name=dest_data['name'],
            defaults=dest_data
        )
        if created:
            print(f"Destination créée: {destination.name}")
        else:
            print(f"Destination existe déjà: {destination.name}")

def populate_club_services():
    """Peupler la base de données avec les services club"""
    services_data = [
        {
            'title': 'Animation en Cascade',
            'description': 'Des activités variées pour tous les âges, de l\'aquagym aux spectacles en soirée',
            'icon_class': 'fas fa-theater-masks',
            'order': 1,
        },
        {
            'title': 'Le Confort Avant Tout',
            'description': 'Chambres spacieuses et services premium pour un séjour inoubliable',
            'icon_class': 'fas fa-bed',
            'order': 2,
        },
        {
            'title': 'Tout Inclus',
            'description': 'Pension complète, boissons et collations disponibles toute la journée',
            'icon_class': 'fas fa-utensils',
            'order': 3,
        },
        {
            'title': 'Vos Enfants sont Rois',
            'description': 'Clubs enfants avec animateurs qualifiés et espaces dédiés',
            'icon_class': 'fas fa-child',
            'order': 4,
        },
        {
            'title': 'Restauration Délicieuse',
            'description': 'Buffets variés et restaurants thématiques avec cuisine locale et internationale',
            'icon_class': 'fas fa-wine-glass-alt',
            'order': 5,
        },
        {
            'title': 'Détente & Bien-être',
            'description': 'Espaces spa, piscines et zones de relaxation pour se ressourcer',
            'icon_class': 'fas fa-spa',
            'order': 6,
        },
    ]

    for service_data in services_data:
        service, created = ClubService.objects.get_or_create(
            title=service_data['title'],
            defaults=service_data
        )
        if created:
            print(f"Service créé: {service.title}")
        else:
            print(f"Service existe déjà: {service.title}")

def populate_special_offers():
    """Peupler la base de données avec les offres spéciales"""
    offers_data = [
        {
            'title': 'Départs Juillet 2025',
            'offer_type': 'discount',
            'badge_text': '-20% Réduction',
            'description': 'Réservez maintenant et bénéficiez de 20% de réduction sur tous nos séjours Club pour les départs de juillet',
            'conditions': 'Offre valable jusqu\'au 15 juillet 2025',
            'valid_until': date(2025, 7, 15),
        },
        {
            'title': 'Enfant Gratuit',
            'offer_type': 'free_child',
            'badge_text': 'Gratuit Enfant',
            'description': 'Pour tout séjour réservé, le 2ème enfant (- de 12 ans) voyage gratuitement en pension complète',
            'conditions': 'Valable sur une sélection d\'hôtels',
        },
        {
            'title': 'Départs Immédiats',
            'offer_type': 'last_minute',
            'badge_text': 'Dernière Minute',
            'description': 'Profitez de nos offres de dernière minute avec des réductions jusqu\'à 40% pour des départs dans les 15 jours',
            'conditions': 'Selon disponibilités',
        },
    ]

    for offer_data in offers_data:
        offer, created = SpecialOffer.objects.get_or_create(
            title=offer_data['title'],
            defaults=offer_data
        )
        if created:
            print(f"Offre créée: {offer.title}")
        else:
            print(f"Offre existe déjà: {offer.title}")

def populate_testimonials():
    """Peupler la base de données avec les témoignages"""
    testimonials_data = [
        {
            'client_name': 'Marie D.',
            'client_city': 'Paris',
            'rating': 5,
            'comment': 'Un séjour absolument parfait ! L\'organisation était impeccable et le service client exceptionnel. Je recommande vivement Blue Sky Tourism.',
            'is_featured': True,
        },
        {
            'client_name': 'Jean-Pierre L.',
            'client_city': 'Lyon',
            'rating': 5,
            'comment': 'Des années d\'expérience, ça se ressent ! Chaque détail était pensé et l\'équipe disponible 24h/24. Merci pour ces vacances inoubliables.',
            'is_featured': True,
        },
        {
            'client_name': 'Sophie M.',
            'client_city': 'Marseille',
            'rating': 5,
            'comment': 'Les clubs BlueSky sont fantastiques ! Animations, restauration, service... tout était parfait. Nos enfants ont adoré !',
            'is_featured': True,
        },
    ]

    for testimonial_data in testimonials_data:
        testimonial, created = Testimonial.objects.get_or_create(
            client_name=testimonial_data['client_name'],
            client_city=testimonial_data['client_city'],
            defaults=testimonial_data
        )
        if created:
            print(f"Témoignage créé: {testimonial.client_name}")
        else:
            print(f"Témoignage existe déjà: {testimonial.client_name}")

if __name__ == '__main__':
    print("Peuplement de la base de données...")
    populate_destinations()
    populate_club_services()
    populate_special_offers()
    populate_testimonials()
    print("Peuplement terminé!")
