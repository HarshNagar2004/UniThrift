from django.contrib import admin
from .models import Profile, Item, RegistrationFile


@admin.register(RegistrationFile)
class RegistrationFileAdmin(admin.ModelAdmin):
    list_display = ['file', 'uploaded_at']


# Custom Admin for SignUp
@admin.register(Profile)
class SignUpAdmin(admin.ModelAdmin):
    # Add any custom configurations for SignUp if necessary
    list_display = ['firstName', 'lastName', 'registration_number']  # Adjust this based on your fields


# Admin for Item model
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['item_name', 'owner_name', 'selling_price', 'created_at']
    search_fields = ['item_name', 'owner_name', 'contact_number']

    def delete_model(self, request, obj):
        # Optionally delete any associated data if necessary
        super().delete_model(request, obj)  # Call the default delete method
