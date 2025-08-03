
from django import forms
from .models import VehicleBooking, Vehicle


from django import forms
from .models import VehicleBooking, Vehicle

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            'vehicle_type', 'make_model', 'year', 'license_plate', 'fuel_type',
            'seating_capacity', 'ac_available', 'gps_enabled',
            'insurance_valid_until', 'pollution_certificate_valid_until',
            'current_location', 'image', 'contact_info', 'description'
        ]
        widgets = {
            'vehicle_type': forms.Select(attrs={'class': 'form-control'}),
            'make_model': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'license_plate': forms.TextInput(attrs={'class': 'form-control'}),
            'fuel_type': forms.Select(attrs={'class': 'form-control'}),
            'seating_capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'ac_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'gps_enabled': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'insurance_valid_until': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'pollution_certificate_valid_until': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'current_location': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'contact_info': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class VehicleBookingForm(forms.ModelForm):
    class Meta:
        model = VehicleBooking
        fields = [
            'vehicle', 'booking_type', 'pickup_location', 'pickup_date', 'pickup_time',
            'dropoff_location', 'return_date', 'return_time', 'contact_phone',
            'passenger_count', 'special_requirements', 'estimated_distance_km',
            'estimated_duration_hours'
        ]
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-control'}),
            'booking_type': forms.Select(attrs={'class': 'form-control'}),
            'pickup_location': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'pickup_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'pickup_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'dropoff_location': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'return_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'return_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'passenger_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'special_requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estimated_distance_km': forms.NumberInput(attrs={'class': 'form-control'}),
            'estimated_duration_hours': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vehicle'].queryset = Vehicle.objects.filter(is_available=True)

class VehicleBookingForm(forms.ModelForm):
    class Meta:
        model = VehicleBooking
        fields = [
            'vehicle', 'booking_type', 'pickup_location', 'pickup_date', 'pickup_time',
            'dropoff_location', 'return_date', 'return_time', 'contact_phone',
            'passenger_count', 'special_requirements', 'estimated_distance_km',
            'estimated_duration_hours'
        ]
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-control'}),
            'booking_type': forms.Select(attrs={'class': 'form-control'}),
            'pickup_location': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'pickup_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'pickup_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'dropoff_location': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'return_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'return_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'passenger_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'special_requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estimated_distance_km': forms.NumberInput(attrs={'class': 'form-control'}),
            'estimated_duration_hours': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vehicle'].queryset = Vehicle.objects.filter(is_available=True)
