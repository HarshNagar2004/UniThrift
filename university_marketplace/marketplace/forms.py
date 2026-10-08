from django import forms
from django.contrib.auth.models import User
from .models import Profile, Item, RegistrationFile


class MySignupForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Re-enter Password")

    class Meta:
        model = Profile
        fields = ['firstName', 'lastName', 'phoneNumber', 'registration_number', 'profile_picture']
        widgets = {
            'firstName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'lastName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'phoneNumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'registration_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Registration Number'}),
            'profile_picture': forms.FileInput(
                attrs={'class': 'form-control', 'placeholder': 'Picture for your profile'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match. Please enter them again.")

        return cleaned_data

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['registration_number'],
            password=self.cleaned_data['password1']
        )
        signup = super().save(commit=False)
        signup.user = user
        if commit:
            signup.save()
        return signup


class MyLogin(forms.Form):
    registration_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'University Registration Number'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['owner_name', 'email', 'item_name', 'item_description', 'age_of_product', 'usage_frequency', 'selling_price',
                  'contact_number', 'image', 'How_many_days_you_want_to_advertise_this_on_the_website']
        widgets = {
            'owner_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Owner Name'}),
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'item_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item Name'}),
            'item_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Item Description'}),
            'age_of_product': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Age of Product'}),
            'usage_frequency': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usage Frequency'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Selling Price'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Number'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'How_many_days_you_want_to_advertise_this_on_the_website': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'After how many days you '
                                                                                             'want to remove this '
                                                                                             'item'}),

        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['firstName', 'lastName', 'phoneNumber', 'profile_picture']  # Include only the fields that can be updated
        widgets = {
            'firstName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'lastName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'phoneNumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }
