from django.urls import path
from . import views

app_name = 'interior'

urlpatterns = [
    path('contractors/', views.interior_contractors_list, name='interior_contractors_list'),
    path('contractors/<int:contractor_id>/', views.interior_contractor_detail, name='interior_contractor_detail'),
    path('designers/', views.designer_list, name='designer_list'),
    path('designers/create/', views.designer_create, name='designer_create'),
    path('designers/<int:designer_id>/', views.designer_detail, name='designer_detail'),
    path('designers/<int:designer_id>/edit/', views.designer_edit, name='designer_edit'),
]
