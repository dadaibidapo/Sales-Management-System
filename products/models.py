from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length = 120)
    logo = models.ImageField(upload_to='customers', default='no_picture.jpeg')
    price = models.FloatField(help_text= 'in US dollars $')
    created = models.DateTimeField(auto_now=True)

    def  __str__(self):
        return  f"{self.name}-{self.created.strftime('%d/%m/%Y')}"