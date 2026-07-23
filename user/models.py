from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# class tbl_register(models.Model):
#     name=models.CharField(max_length=50,null=True)
#     email=models.EmailField(primary_key=True)
#     mobile=models.CharField(max_length=20,null=True)
#     password=models.CharField(max_length=200,null=True)
#     password2=models.CharField(max_length=200,null=True)
#     # city=models.CharField(max_length=50,null=True)
#     # address=models.TextField(null=True)


from django.db import models
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="services"
    )
    title = models.CharField(max_length=200)
    short_description = models.TextField(default="")
    long_description = models.TextField(default="")
    image = models.ImageField(upload_to="services/")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title
   
