from django.core.management.base import BaseCommand
from tourism.models import TravelOffer, Destination, Hotel
from decimal import Decimal
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Populate database with travel offers'

    def handle(self, *args, **options):
        self.stdout.write('Creating travel offers...')
        
        # Récupérer quelques destinations existantes
        destinations = Destination.objects.all()[:6]
        
        if not destinations:
            self.stdout.write(self.style.ERROR('No destinations found. Please run populate_db first.'))
            return
        
        offers_data = [
            {
                'title': 'Séjour Dernière Minute - Tunisie',
                'description': 'Profitez de cette offre exceptionnelle pour découvrir la Tunisie ! Séjour tout inclus dans un hôtel 4* en bord de mer avec animations et spa.',
                'destination': destinations[0],  # Tunisie
                'offer_type': 'last_minute',
                'departure_date': date.today() + timedelta(days=15),
                'return_date': date.today() + timedelta(days=22),
                'original_price': Decimal('899.00'),
                'offer_price': Decimal('649.00'),
                'max_participants': 20,
                'min_participants': 2,
                'deposit_percentage': Decimal('30.00'),
                'included_services': '''Vol aller-retour
Hébergement en hôtel 4*
Pension complète
Transferts aéroport-hôtel
Animations quotidiennes
Accès spa et piscine
Assurance voyage''',
                'excluded_services': '''Boissons alcoolisées premium
Excursions optionnelles
Dépenses personnelles
Pourboires''',
                'conditions': 'Offre valable dans la limite des places disponibles. Annulation possible jusqu\'à 7 jours avant le départ.',
                'is_active': True,
                'is_featured': True,
                'booking_deadline': date.today() + timedelta(days=10),
            },
            {
                'title': 'Réservation Anticipée - Grèce 2025',
                'description': 'Réservez dès maintenant votre séjour en Grèce pour l\'été 2025 et bénéficiez d\'un tarif exceptionnel ! Découvrez les îles grecques dans un cadre idyllique.',
                'destination': destinations[5] if len(destinations) > 5 else destinations[0],  # Grèce
                'offer_type': 'early_bird',
                'departure_date': date(2025, 7, 15),
                'return_date': date(2025, 7, 22),
                'original_price': Decimal('1200.00'),
                'offer_price': Decimal('899.00'),
                'max_participants': 30,
                'min_participants': 2,
                'deposit_percentage': Decimal('25.00'),
                'included_services': '''Vol aller-retour
Hébergement en hôtel 5*
Demi-pension
Transferts inclus
Excursion aux îles
Guide francophone
Wi-Fi gratuit''',
                'excluded_services': '''Déjeuners
Boissons aux repas
Excursions optionnelles
Assurance annulation''',
                'conditions': 'Tarif valable pour les réservations avant le 31 mars 2025. Possibilité de paiement en 3 fois sans frais.',
                'is_active': True,
                'is_featured': True,
                'booking_deadline': date(2025, 3, 31),
            },
            {
                'title': 'Offre Famille - Espagne Costa Brava',
                'description': 'Séjour parfait pour les familles ! Hôtel avec club enfants, piscines et animations. Les enfants de moins de 12 ans bénéficient d\'une réduction de 50%.',
                'destination': destinations[1] if len(destinations) > 1 else destinations[0],  # Espagne
                'offer_type': 'family',
                'departure_date': date.today() + timedelta(days=45),
                'return_date': date.today() + timedelta(days=52),
                'original_price': Decimal('750.00'),
                'offer_price': Decimal('650.00'),
                'max_participants': 25,
                'min_participants': 2,
                'deposit_amount': Decimal('200.00'),  # Acompte fixe
                'included_services': '''Vol aller-retour
Hébergement familial
Tout inclus
Club enfants (4-12 ans)
Animations familiales
Piscines et toboggans
Terrain de jeux''',
                'excluded_services': '''Garde d\'enfants privée
Excursions hors hôtel
Soins spa
Location de voiture''',
                'conditions': 'Réduction de 50% pour les enfants de moins de 12 ans. Gratuit pour les moins de 2 ans.',
                'is_active': True,
                'is_featured': False,
                'booking_deadline': date.today() + timedelta(days=30),
            },
            {
                'title': 'Voyage de Noces - Crète Romantique',
                'description': 'Célébrez votre amour dans un cadre exceptionnel ! Séjour romantique en Crète avec suite vue mer, dîners aux chandelles et excursions privées.',
                'destination': destinations[3] if len(destinations) > 3 else destinations[0],  # Crète
                'offer_type': 'honeymoon',
                'departure_date': date.today() + timedelta(days=60),
                'return_date': date.today() + timedelta(days=67),
                'original_price': Decimal('1500.00'),
                'offer_price': Decimal('1299.00'),
                'max_participants': 8,  # 4 couples max
                'min_participants': 2,
                'deposit_percentage': Decimal('40.00'),
                'included_services': '''Vol aller-retour
Suite romantique vue mer
Demi-pension gastronomique
Dîner romantique privé
Massage couple au spa
Excursion coucher de soleil
Champagne d\'accueil''',
                'excluded_services': '''Déjeuners
Boissons alcoolisées
Excursions supplémentaires
Soins spa individuels''',
                'conditions': 'Offre réservée aux couples. Certificat de mariage requis (moins de 6 mois).',
                'is_active': True,
                'is_featured': True,
                'booking_deadline': date.today() + timedelta(days=45),
            },
            {
                'title': 'Groupe Amis - Canaries Party',
                'description': 'Partez entre amis aux Canaries ! Hébergement en appartements, soirées organisées et activités de groupe. Ambiance garantie !',
                'destination': destinations[2] if len(destinations) > 2 else destinations[0],  # Canaries
                'offer_type': 'group',
                'departure_date': date.today() + timedelta(days=30),
                'return_date': date.today() + timedelta(days=35),
                'original_price': Decimal('599.00'),
                'offer_price': Decimal('499.00'),
                'max_participants': 16,
                'min_participants': 6,
                'deposit_percentage': Decimal('35.00'),
                'included_services': '''Vol aller-retour
Appartements équipés
Transferts groupes
Soirées organisées
Activités nautiques
Guide accompagnateur
Assurance groupe''',
                'excluded_services': '''Repas (cuisine équipée)
Boissons en soirée
Excursions individuelles
Caution appartements''',
                'conditions': 'Minimum 6 personnes. Réduction de 10% à partir de 10 personnes.',
                'is_active': True,
                'is_featured': False,
                'booking_deadline': date.today() + timedelta(days=20),
            },
            {
                'title': 'Offre Senior - Djerba Détente',
                'description': 'Séjour spécialement conçu pour les seniors ! Rythme adapté, excursions culturelles et soins bien-être. Profitez d\'un voyage en toute sérénité.',
                'destination': destinations[4] if len(destinations) > 4 else destinations[0],  # Djerba
                'offer_type': 'senior',
                'departure_date': date.today() + timedelta(days=40),
                'return_date': date.today() + timedelta(days=50),
                'original_price': Decimal('850.00'),
                'offer_price': Decimal('720.00'),
                'max_participants': 15,
                'min_participants': 2,
                'deposit_percentage': Decimal('25.00'),
                'included_services': '''Vol aller-retour
Hôtel 4* calme
Pension complète
Excursions culturelles
Soins thalasso
Accompagnateur senior
Transferts confort''',
                'excluded_services': '''Boissons alcoolisées
Soins spa premium
Excursions optionnelles
Assurance santé''',
                'conditions': 'Réservé aux personnes de plus de 55 ans. Certificat médical recommandé.',
                'is_active': True,
                'is_featured': False,
                'booking_deadline': date.today() + timedelta(days=25),
            },
        ]

        for offer_data in offers_data:
            offer, created = TravelOffer.objects.get_or_create(
                title=offer_data['title'],
                defaults=offer_data
            )
            if created:
                self.stdout.write(f'Created offer: {offer.title}')
            else:
                self.stdout.write(f'Offer already exists: {offer.title}')

        self.stdout.write(self.style.SUCCESS('Travel offers created successfully!'))
