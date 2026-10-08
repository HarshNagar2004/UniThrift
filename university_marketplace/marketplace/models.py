# models.py
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='signup', default=1)
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    registration_number = models.CharField(max_length=30, unique=True)
    phoneNumber = models.CharField(max_length=15, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, default='profile_pictures/d1'
                                                                                                      '.jpg')

    def __str__(self):
        return f"{self.firstName} {self.lastName}"


class Item(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)  # Ensure this refers to the correct user model
    owner_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, null=True, blank=True)  # New email field
    item_name = models.CharField(max_length=100)
    item_description = models.TextField()
    age_of_product = models.CharField(max_length=50)
    usage_frequency = models.CharField(max_length=100)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    contact_number = models.CharField(max_length=15)
    image = models.ImageField(upload_to='item_images/', blank=True, null=True, default='item_images/rolex-1908.webp')
    created_at = models.DateTimeField(auto_now_add=True)
    How_many_days_you_want_to_advertise_this_on_the_website = models.PositiveIntegerField(default=30)  # New field for posting duration

    def __str__(self):
        return f"{self.item_name} by {self.owner_name}"

    def should_delete(self):
        """Check if the item should be deleted based on the posting duration."""
        return timezone.now() >= (self.created_at + timedelta(days=self.days_to_post))


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='chat_images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name}: {self.message[:20]}"


class RegistrationFile(models.Model):
    file = models.FileField(upload_to='registration_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
