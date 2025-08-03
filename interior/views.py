from django.contrib.auth.decorators import login_required
@login_required
def designer_edit(request, designer_id):
    designer = get_object_or_404(InteriorDesigner, id=designer_id)
    if request.method == 'POST':
        form = InteriorDesignerForm(request.POST, request.FILES, instance=designer)
        formset = DesignerGalleryImageFormSet(request.POST, request.FILES, instance=designer)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('interior:designer_detail', designer_id=designer.id)
    else:
        form = InteriorDesignerForm(instance=designer)
        formset = DesignerGalleryImageFormSet(instance=designer)
    return render(request, 'interior/designer_edit.html', {'form': form, 'formset': formset, 'designer': designer})
def interior_contractors_list(request):
    contractors = Contractor.objects.filter(expertise__icontains='interior')
    return render(request, 'interior/contractors_list.html', {'contractors': contractors})
def interior_contractor_detail(request, contractor_id):
    contractor = get_object_or_404(Contractor, id=contractor_id)
    # Gallery images assumed to be in static/images/interior/contractors/<contractor_id>/
    gallery = [f'/static/images/interior/contractors/{contractor_id}/{i}.jpg' for i in range(1, 5)]
    return render(request, 'interior/contractor_detail.html', {'contractor': contractor, 'gallery': gallery})


from django.shortcuts import render, get_object_or_404, redirect
from .models import InteriorDesigner
from .forms import InteriorDesignerForm, DesignerGalleryImageFormSet
import os
from django.conf import settings

def interior_contractors_list(request):
    designers = InteriorDesigner.objects.all()
    # Load background gallery images from static/images/interior/
    gallery_dir = os.path.join(settings.BASE_DIR, 'static', 'images', 'interior')
    gallery_images = []
    if os.path.isdir(gallery_dir):
        for fname in os.listdir(gallery_dir):
            if fname.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                gallery_images.append(f'/static/images/interior/{fname}')
    return render(request, 'interior/designers_gallery.html', {'designers': designers, 'gallery_images': gallery_images})

def designer_create(request):
    if request.method == 'POST':
        form = InteriorDesignerForm(request.POST, request.FILES)
        formset = DesignerGalleryImageFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            designer = form.save()
            formset.instance = designer
            formset.save()
            return redirect('interior:designer_list')
    else:
        form = InteriorDesignerForm()
        formset = DesignerGalleryImageFormSet()
    return render(request, 'interior/designer_create.html', {'form': form, 'formset': formset})

def designer_list(request):
    designers = InteriorDesigner.objects.all()
    return render(request, 'interior/designer_list.html', {'designers': designers})

def designer_detail(request, designer_id):
    designer = get_object_or_404(InteriorDesigner, id=designer_id)
    gallery = designer.gallery_images.all()
    return render(request, 'interior/designer_detail.html', {'designer': designer, 'gallery': gallery})
