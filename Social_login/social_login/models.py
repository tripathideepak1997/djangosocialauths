import os
import urllib

from django.core.files import File
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.utils.safestring import mark_safe

GENDER_CHOICE = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Others')
)


class User(AbstractUser):
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE)
    phone_number = models.BigIntegerField(blank=True, null=True)
    is_phone_verified = models.BooleanField(default=False)
    profile_photo = models.ImageField(upload_to='pic_folder/', default='pic_folder/None/no-img.jpeg')
    url = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        if self.first_name:
            return self.first_name
        return self.username

    def cache(self):
        """Store image locally if we have a URL"""
        if self.url:
            result = urllib.request.urlretrieve(self.url)
            self.profile_photo.save(
                os.path.basename(self.url),
                File(open(result[0], 'rb'))
            )
        self.save()
            
    def image_tag(self):
        return mark_safe('<img src="%s" width=100px height=100px />' % (self.profile_photo.url))

    image_tag.short_description = "image"
    image_tag.allow_tags = True
