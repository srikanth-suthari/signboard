from .forms import ContractorBookingForm, ContractorRegistrationForm
# Contractor registration view
def contractor_register(request):
    if request.method == 'POST':
        form = ContractorRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            contractor = form.save()
            
            # Send WhatsApp welcome message to newly registered contractor
            try:
                from utils.whatsapp import send_whatsapp_message
                message = f"""
🎉 Welcome to S&M Urban Services!

Hello {contractor.name},

Your contractor profile has been successfully registered with us!

📋 Profile Details:
👤 Name: {contractor.name}
📧 Email: {contractor.email}
📞 Phone: {contractor.phone}
🏗️ Category: {contractor.category.name}
💼 Experience: {contractor.experience_years} years
💰 Rate: ₹{contractor.hourly_rate}/hour

🔍 What's Next?
• Your profile is under review
• You'll start receiving booking requests soon
• Keep your phone handy for customer inquiries

📞 Need Help?
Contact our support team at 9640695430

Welcome aboard! 🚀

S&M Urban Services
Team
                """.strip()
                
                # Ensure phone number format for WhatsApp (add +91 if not present)
                contractor_phone = contractor.phone
                if not contractor_phone.startswith('+'):
                    contractor_phone = f'+91{contractor_phone}'
                
                send_whatsapp_message(contractor_phone, message)
                messages.success(request, 'Registration successful! Welcome message sent to your WhatsApp. Your profile will be reviewed soon.')
            except Exception as e:
                messages.success(request, f'Registration successful! However, WhatsApp notification failed: {str(e)}. Your profile will be reviewed soon.')
            
            return redirect('contractors:list')
    else:
        form = ContractorRegistrationForm()
    return render(request, 'contractors/register.html', {'form': form})
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Contractor, ContractorCategory, ContractorBooking
from .forms import ContractorBookingForm

def contractor_list(request):
    contractors = Contractor.objects.filter(is_available=True)
    categories = ContractorCategory.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        contractors = contractors.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    # Category filter
    category_id = request.GET.get('category')
    if category_id:
        contractors = contractors.filter(category_id=category_id)
    
    context = {
        'contractors': contractors,
        'categories': categories,
        'search_query': search_query,
        'selected_category': int(category_id) if category_id else None,
    }
    return render(request, 'contractors/list.html', context)

def contractor_detail(request, contractor_id):
    contractor = get_object_or_404(Contractor, id=contractor_id)
    return render(request, 'contractors/detail.html', {'contractor': contractor})

@login_required
def book_contractor(request, contractor_id):
    contractor = get_object_or_404(Contractor, id=contractor_id)
    
    if request.method == 'POST':
        form = ContractorBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.contractor = contractor
            booking.save()
            
            # Send WhatsApp message to contractor
            try:
                from utils.whatsapp import send_whatsapp_message
                message = f"""
🔔 New Booking Request!

👤 Customer: {request.user.first_name} {request.user.last_name}
📞 Phone: {booking.contact_phone}
📧 Email: {request.user.email}

🏗️ Project: {booking.project_title}
📝 Description: {booking.project_description}

💰 Budget: ₹{booking.budget}
⏱️ Duration: {booking.estimated_duration}
📅 Start Date: {booking.preferred_start_date.strftime('%d %B %Y')}
📍 Address: {booking.project_address}

Booking ID: #{booking.id}

Please contact the customer to discuss further details.

S&M Urban Services
                """.strip()
                
                # Ensure phone number format for WhatsApp (add +91 if not present)
                contractor_phone = contractor.phone
                if not contractor_phone.startswith('+'):
                    contractor_phone = f'+91{contractor_phone}'
                
                send_whatsapp_message(contractor_phone, message)
                messages.success(request, 'Booking request submitted successfully! The contractor will contact you soon via WhatsApp.')
            except Exception as e:
                messages.warning(request, f'Booking submitted but WhatsApp notification failed: {str(e)}. The contractor will still receive your booking request.')
            
            return redirect('contractors:booking_detail', booking_id=booking.id)
    else:
        form = ContractorBookingForm()
    
    return render(request, 'contractors/book.html', {
        'contractor': contractor,
        'form': form
    })

@login_required
def my_bookings(request):
    bookings = ContractorBooking.objects.filter(customer=request.user)
    return render(request, 'contractors/my_bookings.html', {'bookings': bookings})

@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(ContractorBooking, id=booking_id, customer=request.user)
    return render(request, 'contractors/booking_detail.html', {'booking': booking})

def category_list(request):
    categories = ContractorCategory.objects.all()
    return render(request, 'contractors/categories.html', {'categories': categories})

def contractors_by_category(request, category_id):
    category = get_object_or_404(ContractorCategory, id=category_id)
    contractors = Contractor.objects.filter(category=category, is_available=True)
    return render(request, 'contractors/by_category.html', {
        'category': category,
        'contractors': contractors
    })
