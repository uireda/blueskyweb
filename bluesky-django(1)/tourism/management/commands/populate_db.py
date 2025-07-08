from django.core.management.base import BaseCommand
from tourism.models import Destination, ClubService, SpecialOffer, Testimonial
from decimal import Decimal
from datetime import date

class Command(BaseCommand):
    help = 'Populate database with initial data'

    def handle(self, *args, **options):
        self.stdout.write('Populating database...')
        
        # Créer les hôtels d'abord
        hotels_data = [
            {
                'name': 'Hotel Yasmine Beach Resort',
                'rating': 4,
                'description': 'Hôtel moderne en bord de mer avec vue panoramique sur la Méditerranée',
                'amenities': 'Piscine, Spa, Restaurant, Bar, WiFi gratuit, Climatisation, Room service',
                'address': 'Zone Touristique Yasmine Hammamet, Tunisie',
                'phone': '+216 72 123 456',
                'email': 'info@yasminebeach.tn',
            },
            {
                'name': 'Porto Cristo Palace',
                'rating': 4,
                'description': 'Hôtel élégant situé près des célèbres grottes du Drach',
                'amenities': 'Piscine extérieure, Restaurant gastronomique, Spa, Salle de fitness, WiFi',
                'address': 'Carrer de Burdils, 07680 Porto Cristo, Majorque',
                'phone': '+34 971 820 450',
                'email': 'reservas@portocristopalace.com',
            },
            {
                'name': 'Costa Adeje Grand Resort',
                'rating': 4,
                'description': 'Resort luxueux avec accès direct à la plage de sable noir',
                'amenities': 'Piscines multiples, Spa thermal, 3 restaurants, Bar de plage, Tennis, Golf',
                'address': 'Avenida de Bruselas, 38660 Costa Adeje, Tenerife',
                'phone': '+34 922 750 200',
                'email': 'info@costadejeresort.es',
            },
            {
                'name': 'Bali Beach Hotel Crete',
                'rating': 3,
                'description': 'Hôtel familial avec vue sur la mer Égée et plage privée',
                'amenities': 'Piscine, Restaurant traditionnel, Bar, WiFi, Parking gratuit',
                'address': 'Bali Beach, 74057 Bali, Crète, Grèce',
                'phone': '+30 28340 94210',
                'email': 'info@balibeachcrete.gr',
            },
            {
                'name': 'Djerba Sun Club',
                'rating': 4,
                'description': 'Club de vacances tout inclus sur l\'île de Djerba',
                'amenities': 'Animation, Piscines, Restaurants multiples, Sports nautiques, Spa, Kids club',
                'address': 'Zone Touristique Sidi Mahres, Djerba, Tunisie',
                'phone': '+216 75 757 000',
                'email': 'contact@djerbasunclub.tn',
            },
            {
                'name': 'Vravrona Bay Resort',
                'rating': 5,
                'description': 'Resort de luxe 5 étoiles avec vue sur la baie de Vravrona',
                'amenities': 'Spa de luxe, Piscine infinity, Restaurant gastronomique, Plage privée, Concierge',
                'address': 'Vravrona Bay, 19003 Vravrona, Grèce',
                'phone': '+30 22990 89000',
                'email': 'reservations@vravronaresort.gr',
            },
        ]

        from tourism.models import Hotel
        for hotel_data in hotels_data:
            hotel, created = Hotel.objects.get_or_create(
                name=hotel_data['name'],
                defaults=hotel_data
            )
            if created:
                self.stdout.write(f'Created hotel: {hotel.name}')

        # Maintenant créer les destinations avec les hôtels
        destinations_data = [
            {
                'name': 'Tunisie - Yasmine Hammamet',
                'location': 'Yasmine Hammamet',
                'hotel_names': ['Hotel Yasmine Beach Resort'],
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
                'hotel_names': ['Porto Cristo Palace'],
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
                'hotel_names': ['Costa Adeje Grand Resort'],
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
                'hotel_names': ['Bali Beach Hotel Crete'],
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
                'hotel_names': ['Djerba Sun Club'],
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
                'hotel_names': ['Vravrona Bay Resort'],
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
            hotel_names = dest_data.pop('hotel_names')
            
            destination, created = Destination.objects.get_or_create(
                name=dest_data['name'],
                defaults=dest_data
            )
            
            if created:
                # Ajouter les hôtels à la destination
                for hotel_name in hotel_names:
                    try:
                        hotel = Hotel.objects.get(name=hotel_name)
                        destination.hotels.add(hotel)
                    except Hotel.DoesNotExist:
                        self.stdout.write(f'Hotel {hotel_name} not found')
                
                self.stdout.write(f'Created destination: {destination.name}')

        # Créer les services club
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
                self.stdout.write(f'Created service: {service.title}')

        # Créer les offres spéciales
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
                self.stdout.write(f'Created offer: {offer.title}')

        # Créer les témoignages
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
                self.stdout.write(f'Created testimonial: {testimonial.client_name}')

        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))
