from django import forms
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from .models import SearchQuery

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
