from django.contrib import admin
from .models import Donor, Fundraiser, Campaign, Donation, Contact


@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username', 'email', 'contact_info')
    search_fields = ('first_name', 'last_name', 'username', 'email')
   


@admin.register(Fundraiser)
class FundraiserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username', 'email', 'contact_info', 'country')
    search_fields = ('first_name', 'last_name', 'username', 'email')
 

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'fundraiser', 'target_amount', 'deadline', 'category_id')
    search_fields = ('title', 'fundraiser__username', 'category_id')



@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('donor', 'campaign', 'amount', 'date')
    search_fields = ('donor__username', 'campaign__title')
   


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message')
    search_fields = ('name', 'email')
  
