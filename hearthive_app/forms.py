from django import forms
from .models import Donor
from .models import Fundraiser, Campaign, Donation, Contact



class DonorModelForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'contact_info', 'account_balance', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            'contact_info': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Contact Info'}),
            'account_balance': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Account Balance'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'username': None, 
        }






class FundraiserModelForm(forms.ModelForm):
    class Meta:
        model = Fundraiser
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'contact_info', 'country', 'profile_picture']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'contact_info': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Info'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Info'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'username': None,
        }



class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['title', 'description', 'image', 'deadline', 'target_amount', 'category_id']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Campaign Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe your campaign'}),
            'target_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Target Amount'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'category_id': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['amount']




class FundraiserUpdateForm(forms.ModelForm):
    class Meta:
        model = Fundraiser
        fields = ['first_name', 'last_name', 'email', 'contact_info', 'country', 'profile_picture']  # Excluding password

class DonorUpdateForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['first_name', 'last_name', 'email', 'contact_info', 'account_balance', 'profile_picture']





class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'placeholder': 'Your Message', 'class': 'form-control', 'rows': 5}),
        }
