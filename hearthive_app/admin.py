from django.contrib import admin
from .models import Donor, Fundraiser, User, Campaign, Donation, Payment, Contact


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email')
    search_fields = ('id', 'username', 'email', 'first_name', 'last_name')

class DonorAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'contact_info', 'account_balance')
    search_fields = ('id', 'username', 'email', 'first_name', 'last_name')

class FundraiserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'contact_info', 'country')
    search_fields = ('id', 'username', 'first_name', 'last_name', 'email')


class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'fundraiser', 'status', 'category_id', 'target_amount', 'date_created', 'deadline')
    list_filter = ('status', 'category_id')
    search_fields = ('title', 'fundraiser__username')
    actions = ['approve_campaign']


    def approve_campaign(self, request, queryset):
        queryset.update(status='Active')
    approve_campaign.short_description = 'Approve selected campaigns'

class DonationAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'donor', 'amount', 'date')
    list_filter = ('campaign', 'donor')
    search_fields = ('campaign__title', 'donor__username')


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('donor', 'campaign', 'amount', 'transaction_date')
    list_filter = ('campaign', 'donor')
    search_fields = ('campaign__title', 'donor__username')



class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message')
    list_filter = ('name', 'email')
    search_fields = ('name', 'email')





admin.site.register(User, UserAdmin)
admin.site.register(Donor, DonorAdmin)
admin.site.register(Fundraiser, FundraiserAdmin)
admin.site.register(Campaign, CampaignAdmin)  
admin.site.register(Donation, DonationAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Contact, ContactAdmin)
