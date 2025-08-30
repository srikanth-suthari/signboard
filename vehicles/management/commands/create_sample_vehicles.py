from django.core.management.base import BaseCommand
from vehicles.models import Vehicle, VehicleType
from django.contrib.auth.models import User
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Create sample vehicles to display all available images'

    def handle(self, *args, **options):
        # Get or create a default vehicle type
        vehicle_type, created = VehicleType.objects.get_or_create(
            name='Standard Car',
            defaults={
                'description': 'Standard passenger vehicle',
                'capacity': '4-5 passengers',
                'base_rate_per_hour': 500.00,
                'base_rate_per_km': 15.00,
            }
        )

        # Get or create a default user as owner
        user, created = User.objects.get_or_create(
            username='demo_owner',
            defaults={
                'email': 'demo@example.com',
                'first_name': 'Demo',
                'last_name': 'Owner',
            }
        )

        # Vehicle data matching our image files
        vehicles_data = [
            {
                'make_model': 'Maruti Suzuki Swift',
                'license_plate': 'MH12AB1234',
                'year': 2022,
                'fuel_type': 'petrol',
                'seating_capacity': 5,
                'current_location': 'Mumbai',
            },
            {
                'make_model': 'Toyota Innova',
                'license_plate': 'MH12CD5678',
                'year': 2023,
                'fuel_type': 'diesel',
                'seating_capacity': 7,
                'current_location': 'Delhi',
            },
            {
                'make_model': 'Tata Ace',
                'license_plate': 'MH12EF9012',
                'year': 2021,
                'fuel_type': 'diesel',
                'seating_capacity': 3,
                'current_location': 'Pune',
            },
            {
                'make_model': 'Honda Activa',
                'license_plate': 'MH12GH3456',
                'year': 2022,
                'fuel_type': 'petrol',
                'seating_capacity': 2,
                'current_location': 'Bangalore',
            },
            {
                'make_model': 'Maruti Suzuki Swift Dezire',
                'license_plate': 'MH12IJ7890',
                'year': 2023,
                'fuel_type': 'petrol',
                'seating_capacity': 5,
                'current_location': 'Chennai',
            },
            {
                'make_model': 'swift_dezire',
                'license_plate': 'MH12KL1122',
                'year': 2022,
                'fuel_type': 'petrol',
                'seating_capacity': 5,
                'current_location': 'Hyderabad',
            },
        ]

        created_count = 0
        for vehicle_data in vehicles_data:
            # Check if vehicle with this license plate already exists
            if not Vehicle.objects.filter(license_plate=vehicle_data['license_plate']).exists():
                Vehicle.objects.create(
                    vehicle_type=vehicle_type,
                    owner=user,
                    make_model=vehicle_data['make_model'],
                    license_plate=vehicle_data['license_plate'],
                    year=vehicle_data['year'],
                    fuel_type=vehicle_data['fuel_type'],
                    seating_capacity=vehicle_data['seating_capacity'],
                    current_location=vehicle_data['current_location'],
                    insurance_valid_until=date.today() + timedelta(days=365),
                    pollution_certificate_valid_until=date.today() + timedelta(days=180),
                    is_available=True,
                    ac_available=True,
                    gps_enabled=True,
                    contact_info='9876543210',
                    description=f'Well maintained {vehicle_data["make_model"]} available for rental',
                )
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created vehicle: {vehicle_data["make_model"]} - {vehicle_data["license_plate"]}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Vehicle already exists: {vehicle_data["license_plate"]}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} vehicles with corresponding images')
        )
