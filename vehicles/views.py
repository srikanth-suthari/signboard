from utils.whatsapp import send_whatsapp_message
import os
from django.conf import settings
# Vehicle gallery view
def vehicles_gallery(request):
    # List of static vehicle images (match files in static/images/vehicles)
    vehicle_images = [
        'Tata Ace.jpg',
        'Toyota Innova.jpg',
        'Honda Activa.jpg',
        'Maruti Suzuki Swift.jpg',
        'Maruti Suzuki Swift Dezire.jpg',
    ]
    return render(request, 'vehicles/gallery.html', {'vehicle_images': vehicle_images})
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Vehicle, VehicleType, VehicleBooking, Driver
from .forms import VehicleBookingForm, VehicleForm
from django.db.models import Q
from django.contrib.auth.models import User
@login_required
def upload_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.owner = request.user
            vehicle.save()
            messages.success(request, 'Your vehicle has been submitted for rental!')
            return redirect('vehicles:list')
    else:
        form = VehicleForm()
    return render(request, 'vehicles/upload.html', {'form': form})
import uuid

def vehicle_list(request):
    vehicles = Vehicle.objects.filter(is_available=True)

    # Exclude specific make_model entries
    exclude_models = [
        'Hyundai i20',
        'Honda City',
        'Mahindra Scorpio',
        'Bajaj Pulsar',
        'Maruthi Ciaz zeta',
    ]
    from django.db.models import Q
    exclude_q = Q()
    for m in exclude_models:
        exclude_q |= Q(make_model__iexact=m)
    vehicles = vehicles.exclude(exclude_q)

    # Exclude vehicles with license plates matching pattern MH##XX#### (state code + numbers)
    import re
    vehicles_to_exclude = []
    for vehicle in vehicles:
        if vehicle.license_plate and re.match(r'^[A-Z]{2}\d{2}[A-Z]{2}\d{4}$', vehicle.license_plate):
            vehicles_to_exclude.append(vehicle.id)

    if vehicles_to_exclude:
        vehicles = vehicles.exclude(id__in=vehicles_to_exclude)

    vehicle_types = VehicleType.objects.all()

    # Filter by type
    type_filter = request.GET.get('type')
    if type_filter:
        vehicles = vehicles.filter(vehicle_type_id=type_filter)

    # Filter by fuel type
    fuel_filter = request.GET.get('fuel')
    if fuel_filter:
        vehicles = vehicles.filter(fuel_type=fuel_filter)

    # Filter by AC
    ac_filter = request.GET.get('ac')
    if ac_filter == '1':
        vehicles = vehicles.filter(ac_available=True)

    # Filter by location
    location_filter = request.GET.get('location')
    if location_filter:
        vehicles = vehicles.filter(current_location__icontains=location_filter)

    # Separate vehicles with and without images
    vehicles_with_images = list(vehicles.filter(image__isnull=False))
    vehicles_without_images_qs = vehicles.filter(image__isnull=True)

    # Static images to use as fallbacks (match files in static/images/vehicles)
    static_images = ['Tata Ace.jpg', 'Toyota Innova.jpg', 'Honda Activa.jpg', 'Maruti Suzuki Swift.jpg', 'Maruti Suzuki Swift Dezire.jpg']

    # Special mapping: exact make_model (lowercase, trimmed) -> filename
    special_map = {
        'maruti suzuki swift': 'Maruti Suzuki Swift.jpg',
        'toyota innova': 'Toyota Innova.jpg',
        'tata ace': 'Tata Ace.jpg',
        'honda activa': 'Honda Activa.jpg',
        'maruti suzuki swift dezire': 'Maruti Suzuki Swift Dezire.jpg',
        'swift dezire': 'Maruti Suzuki Swift Dezire.jpg',
    }

    # Create dummy vehicle objects to ensure all images are displayed

    # Get or create default vehicle type and user
    try:
        default_vehicle_type = VehicleType.objects.first()
        if not default_vehicle_type:
            default_vehicle_type = VehicleType.objects.create(
                name='Standard Vehicle',
                description='Standard vehicle type',
                capacity='4-5 passengers',
                base_rate_per_hour=500,
                base_rate_per_km=15
            )

        demo_user = User.objects.filter(username='demo_user').first()
        if not demo_user:
            demo_user = User.objects.create_user(
                username='demo_user',
                email='demo@example.com',
                first_name='Demo',
                last_name='User'
            )
    except:
        # If there's any issue with database operations, continue with existing logic
        pass

    # Ensure we have vehicles for each image by creating virtual ones if needed
    vehicle_image_pairs = [
        ('Maruti Suzuki Swift', 'Maruti Suzuki Swift.jpg'),
        ('Toyota Innova', 'Toyota Innova.jpg'),
        ('Tata Ace', 'Tata Ace.jpg'),
        ('Honda Activa', 'Honda Activa.jpg'),
        ('Maruti Suzuki Swift Dezire', 'Maruti Suzuki Swift Dezire.jpg'),
    ]

    # Build list of vehicles without images, assigning unique static images and honoring special_map (exact match)
    vehicles_without_images = []
    used_images = set()
    vehicles_without_images_list = list(vehicles_without_images_qs)

    # First, handle existing vehicles without images
    for v in vehicles_without_images_list:
        m = (v.make_model or '').lower().strip()
        assigned = False
        # Exact match first
        if m in special_map and special_map[m] not in used_images:
            img = special_map[m]
            vehicles_without_images.append((v, img))
            used_images.add(img)
            assigned = True
        else:
            # Fallback: case-insensitive substring match (key in model or model in key)
            for key, img in special_map.items():
                if img in used_images:
                    continue
                if key in m or m in key:
                    vehicles_without_images.append((v, img))
                    used_images.add(img)
                    assigned = True
                    break

    # Then assign remaining static images to other vehicles without images, avoiding reuse
    for v in vehicles_without_images_list:
        if any(v is x[0] for x in vehicles_without_images):
            continue
        # pick next unused image
        img = None
        for s in static_images:
            if s not in used_images:
                img = s
                break
        if img:
            vehicles_without_images.append((v, img))
            used_images.add(img)
        # stop when we've used all static images
        if len(used_images) >= len(static_images):
            break

    # If we still have unused images, create virtual vehicles for them
    if len(used_images) < len(static_images) and 'default_vehicle_type' in locals() and 'demo_user' in locals():
        for make_model, img_filename in vehicle_image_pairs:
            if img_filename not in used_images:
                # Create a virtual vehicle object (not saved to database)
                virtual_vehicle = Vehicle(
                    vehicle_type=default_vehicle_type,
                    make_model=make_model,
                    license_plate=f'DEMO{len(vehicles_without_images):04d}',
                    year=2023,
                    fuel_type='petrol',
                    seating_capacity=5,
                    ac_available=True,
                    gps_enabled=True,
                    is_available=True,
                    current_location='Available',
                    contact_info='Contact for details',
                    description=f'Sample {make_model} vehicle',
                    owner=demo_user
                )
                vehicles_without_images.append((virtual_vehicle, img_filename))
                used_images.add(img_filename)

    # Combine the final vehicles list: keep vehicles with their images first, then ones without images (paired with assigned fallback)
    # For template compatibility, we'll convert vehicles_without_images to wrapper objects with a 'fallback_image' attribute
    final_vehicles = []
    final_vehicles.extend(vehicles_with_images)
    for v, img in vehicles_without_images:
        # store full path so template can call {% static vehicle.fallback_image %}
        setattr(v, 'fallback_image', f'images/vehicles/{img}')
        final_vehicles.append(v)

    vehicles = final_vehicles

    # For location dropdown
    locations = Vehicle.objects.values_list('current_location', flat=True).distinct()

    context = {
        'vehicles': vehicles,
        'vehicle_types': vehicle_types,
        'selected_type': int(type_filter) if type_filter else None,
        'selected_fuel': fuel_filter,
        'ac_only': ac_filter == '1',
        'fuel_choices': Vehicle.FUEL_CHOICES,
        'locations': locations,
        'selected_location': location_filter,
    }
    return render(request, 'vehicles/list.html', context)

@login_required
def book_vehicle(request):
    if request.method == 'POST':
        form = VehicleBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.booking_number = f'VH{uuid.uuid4().hex[:8].upper()}'
            booking.save()

            # Calculate fare
            booking.calculate_fare()
            booking.save()

            # WhatsApp notification to vehicle owner
            owner = booking.vehicle.owner
            if owner and hasattr(owner, 'profile') and getattr(owner.profile, 'phone', None):
                owner_phone = owner.profile.phone  # Should be in international format, e.g., +919640695430
                msg = f"New booking for your vehicle {booking.vehicle.make_model} ({booking.vehicle.license_plate}). Booking No: {booking.booking_number}."
                try:
                    send_whatsapp_message(owner_phone, msg)
                except Exception as e:
                    pass  # Optionally log error

            messages.success(request, f'Booking request submitted! Booking number: {booking.booking_number}')
            return redirect('vehicles:booking_detail', booking_id=booking.id)
    else:
        form = VehicleBookingForm()

    return render(request, 'vehicles/book.html', {'form': form})

@login_required
def my_bookings(request):
    bookings = VehicleBooking.objects.filter(customer=request.user)
    return render(request, 'vehicles/my_bookings.html', {'bookings': bookings})

@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(VehicleBooking, id=booking_id, customer=request.user)
    return render(request, 'vehicles/booking_detail.html', {'booking': booking})

def vehicle_types(request):
    types = VehicleType.objects.all()
    return render(request, 'vehicles/types.html', {'types': types})

def calculate_fare(request):
    if request.method == 'GET':
        vehicle_id = request.GET.get('vehicle_id')
        booking_type = request.GET.get('booking_type')
        distance_km = float(request.GET.get('distance_km', 0))
        duration_hours = float(request.GET.get('duration_hours', 0))

        try:
            vehicle = Vehicle.objects.get(id=vehicle_id)
            vehicle_type = vehicle.vehicle_type

            base_fare = 100  # Base booking fee
            distance_fare = distance_km * vehicle_type.base_rate_per_km

            if booking_type == 'hourly':
                time_fare = duration_hours * vehicle_type.base_rate_per_hour
            else:
                time_fare = 0

            # Additional charges for airport transfers
            additional_charges = 200 if booking_type == 'airport_transfer' else 0

            total_fare = base_fare + distance_fare + time_fare + additional_charges

            return JsonResponse({
                'success': True,
                'base_fare': float(base_fare),
                'distance_fare': float(distance_fare),
                'time_fare': float(time_fare),
                'additional_charges': float(additional_charges),
                'total_fare': float(total_fare)
            })

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request'})
