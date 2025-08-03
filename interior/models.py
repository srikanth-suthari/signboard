from django.db import models

class InteriorDesigner(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.TextField()
    profile_image = models.ImageField(upload_to='designer_profiles/', blank=True, null=True)

    def __str__(self):
        return self.name

class DesignerGalleryImage(models.Model):
    designer = models.ForeignKey(InteriorDesigner, related_name='gallery_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='designer_galleries/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.designer.name} - {self.image.name}"
