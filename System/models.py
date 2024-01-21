from django.db import models


# Create your models here.
#  why and when we use python manage.py flush, search it
# python manage.py shell
# some queries in __ called look up for example loc = Location.objects.get(jobs__title__startswith='p')
# loc = Location.objects.get(jobs__title__contains='task')
# loc = Location.objects.get(jobs__title='python task 1')
# .get used for finding one thing
# .filter used for multiple things
# if data already exist in some model, then you use some one field inwhich attribute is unique=True, then your database will crash out because of existing data
# For creating OneToOne and ManyToOne and ManyToMany relationship illustrate it
class customer(models.Model):
    name = models.CharField(max_length=25)
    email = models.EmailField()

    def __str__(self):
        return self.name


#  this model is used for OneToOne relation with Jobs model
class Location(models.Model):
    state = models.CharField(max_length=25)
    postal_code = models.IntegerField()
    city = models.CharField(max_length=25)
    country = models.CharField(max_length=25)

    def __str__(self):
        return f'{self.id}, {self.state}, {self.postal_code}, {self.city}, {self.country}'


#  this model is used for ManyToOne relationship with  Jobs model
class Author(models.Model):
    name = models.CharField(max_length=25)
    company = models.CharField(max_length=25)

    def __str__(self):
        return f'{self.id}, {self.name}, {self.company}'


#  this model is used to ManyToMany relationship with Jobs
class Skill(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return f'{self.id},{self.name}'

# for creating slug so must import slugify
from django.utils.text import slugify


class Jobs(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ("Open", "Open"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed")
    ])

    date = models.DateField()
    # here Location model connected with Jobs model by OneToOne field, remember it always itself unique, can check in DB Browser for SQLite
    location = models.OneToOneField(Location, on_delete=models.CASCADE, null=True)
    # here Author model connected with Jobs model by ManyToOne relation as ForeignKey, remember it always not itself unique
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    # here Skill model connected with Jobs model by ManyToMany relation, remember it always not itself unique, no cascade, no null
    skill = models.ManyToManyField(Skill)
    slug = models.SlugField(null=True, unique=True, max_length=40)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super(Jobs, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


from django.contrib.auth.models import User


class extended(models.Model):
    id = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    img = models.ImageField()

    def __str__(self):
        return str(self.id)


from django.db.models.signals import pre_delete
from django.dispatch import receiver
import os


# make signals to delete image from database and static folder
@receiver(pre_delete, sender=User)
def remove_picture(sender, instance, **kwargs):
    try:
        os.remove(instance.extended.img.path)
    except:
        pass


class Book(models.Model):
    title = models.CharField(max_length=25)
    author = models.CharField(max_length=25)

    def __str__(self):
        return self.title


class Contact_form(models.Model):
    name = models.CharField(max_length=35)
    email = models.EmailField()
    message = models.TextField(max_length=550)

    def __str__(self):
        return self.name


# model for upload document on upload_blog
class Document(models.Model):
    title = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=445, blank=True)
    document = models.FileField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description
