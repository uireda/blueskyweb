from django.core.management.base import BaseCommand
from tourism.models import Destination, ClubService, SpecialOffer, Testimonial
from decimal import Decimal
from datetime import date

class Command(BaseCommand):
    help = 'Populate database with initial data'

    def handle(self, *args, **options):
        self.stdout.write('Populating database...')
        
        # Créer les destinations
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
            # Ajouter les autres destinations...
        ]

        for dest_data in destinations_data:
            destination, created = Destination.objects.get_or_create(
                name=dest_data['name'],
                defaults=dest_data
            )
            if created:
                self.stdout.write(f'Created destination: {destination.name}')

        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))
