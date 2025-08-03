from django import forms
from .models import Contractor

class ContractorRegistrationForm(forms.ModelForm):
    class Meta:
        model = Contractor
        fields = [
            'name', 'email', 'phone', 'address', 'expertise', 'category', 'description',
            'experience_years', 'hourly_rate', 'profile_image'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'expertise': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'hourly_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
from django import forms
from django import forms
from .models import ContractorBooking, Contractor

class ContractorBookingForm(forms.ModelForm):
    class Meta:
        model = ContractorBooking
        fields = [
            'project_title', 'project_description', 'estimated_duration',
            'budget', 'contact_phone', 'project_address', 'preferred_start_date'
        ]
        widgets = {
            'project_title': forms.TextInput(attrs={'class': 'form-control'}),
            'project_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'estimated_duration': forms.TextInput(attrs={'class': 'form-control'}),
            'budget': forms.NumberInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'project_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'preferred_start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
