from django.db import models
from user_app.models import Author, Book


#from user_app.models import Author, Book

class CarouselImage(models.Model):
    image = models.ImageField(upload_to='carousel_images/', null=True, blank=True)
    title = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title if self.title else "Carousel Image"
    



