from django import forms
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from .models import SearchQuery, OfferReservation, TravelOffer

class SearchForm(forms.ModelForm):
    class Meta:
        model = SearchQuery
        fields = ['destination', 'departure_date', 'duration', 'travelers_count', 'email', 'phone']
        widgets = {
            'destination': forms.Select(attrs={
                'class': 'form-control',
                'id': 'destination'
            }),
            'departure_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'id': 'depart'
            }),
            'duration': forms.Select(attrs={
                'class': 'form-control',
                'id': 'duree'
            }),
            'travelers_count': forms.Select(
                choices=[(i, f"{i} personne{'s' if i > 1 else ''}") for i in range(1, 11)],
                attrs={
                    'class': 'form-control',
                    'id': 'personnes'
                }
            ),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre email (optionnel)'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre téléphone (optionnel)'
            })
        }

    def clean_departure_date(self):
        departure_date = self.cleaned_data['departure_date']
        if departure_date < date.today():
            raise ValidationError("La date de départ ne peut pas être dans le passé.")
        if departure_date > date.today() + timedelta(days=365):
            raise ValidationError("La date de départ ne peut pas être plus d'un an dans le futur.")
        return departure_date

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre nom complet'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre email'
        })
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre téléphone (optionnel)'
        })
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Sujet de votre message'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Votre message'
        })
    )

class OfferReservationForm(forms.ModelForm):
    PAYMENT_CHOICES = [
        ('deposit', 'Payer un acompte seulement'),
        ('full', 'Payer le montant total'),
    ]
    
    payment_type = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect,
        initial='deposit',
        label="Type de paiement"
    )
    
    class Meta:
        model = OfferReservation
        fields = ['client_name', 'client_email', 'client_phone', 'participants_count', 'special_requests', 'payment_type']
        widgets = {
            'client_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom complet'}),
            'client_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'votre@email.com'}),
            'client_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+33 6 12 34 56 78'}),
            'participants_count': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Demandes particulières (optionnel)'}),
        }
        labels = {
            'client_name': 'Nom complet',
            'client_email': 'Adresse email',
            'client_phone': 'Téléphone',
            'participants_count': 'Nombre de participants',
            'special_requests': 'Demandes spéciales',
        }

    def __init__(self, *args, **kwargs):
        self.offer = kwargs.pop('offer', None)
        super().__init__(*args, **kwargs)
        
        if self.offer:
            self.fields['participants_count'].widget.attrs['max'] = self.offer.available_spots
            self.fields['participants_count'].help_text = f"Maximum {self.offer.available_spots} places disponibles"

    def clean_participants_count(self):
        participants_count = self.cleaned_data['participants_count']
        if self.offer and participants_count > self.offer.available_spots:
            raise forms.ValidationError(f"Seulement {self.offer.available_spots} places disponibles")
        if self.offer and participants_count < self.offer.min_participants:
            raise forms.ValidationError(f"Minimum {self.offer.min_participants} participants requis")
        return participants_count
