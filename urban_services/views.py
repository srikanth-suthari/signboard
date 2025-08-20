import os
from django.conf import settings
from django.shortcuts import render

def home(request):
    # List all images in static/images/interior/
    interior_dir = os.path.join(settings.BASE_DIR, 'static', 'images', 'interior')
    images = []
    if os.path.isdir(interior_dir):
        for fname in sorted(os.listdir(interior_dir)):
            if fname.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif')):
                images.append(f'/static/images/interior/{fname}')

    # Pick a random contractor image from static/images/contractors/
    import random
    contractor_dir = os.path.join(settings.BASE_DIR, 'static', 'images', 'contractors')
    contractor_images = []
    if os.path.isdir(contractor_dir):
        for fname in os.listdir(contractor_dir):
            if fname.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif')):
                contractor_images.append(f'/static/images/contractors/{fname}')
    # Ensure the fallback has a leading slash so templates resolve it as an absolute path
    contractor_image = random.choice(contractor_images) if contractor_images else '/static/images/contractors/1.jpg'

    # List all images in static/images/signboards/
    signboard_dir = os.path.join(settings.BASE_DIR, 'static', 'images', 'signboards')
    signboard_images = []
    if os.path.isdir(signboard_dir):
        for fname in sorted(os.listdir(signboard_dir)):
            if fname.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif')):
                signboard_images.append(f'/static/images/signboards/{fname}')

    # List all images in static/images/vehicles/
    vehicle_dir = os.path.join(settings.BASE_DIR, 'static', 'images', 'vehicles')
    vehicle_images = []
    if os.path.isdir(vehicle_dir):
        for fname in sorted(os.listdir(vehicle_dir)):
            if fname.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif')):
                vehicle_images.append(f'/static/images/vehicles/{fname}')

    return render(request, 'home.html', {
        'interior_images': images,
        'contractor_image': contractor_image,
        'signboard_images': signboard_images,
        'vehicle_images': vehicle_images,
    })
