from django import forms
from .models import InteriorDesigner, DesignerGalleryImage

class InteriorDesignerForm(forms.ModelForm):
    class Meta:
        model = InteriorDesigner
        fields = ['name', 'contact_info', 'profile_image']


class DesignerGalleryImageForm(forms.ModelForm):
    class Meta:
        model = DesignerGalleryImage
        fields = ['image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False

DesignerGalleryImageFormSet = forms.inlineformset_factory(
    InteriorDesigner, DesignerGalleryImage, form=DesignerGalleryImageForm,
    extra=10, can_delete=True
)
