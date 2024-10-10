from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    contact_info = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='images/profile_pics/', blank=True, null=True)
    email = models.EmailField(default='example@gmail.com')


class Donor(User):




    class Meta:
        verbose_name = 'Donor'


class Fundraiser(User):
    country = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Fundraiser'


class Campaign(models.Model):
    STATUS_CHOICES = [
        ('Pending Approval', 'Pending Approval'),
    ]

    CATEGORY_CHOICES = [
        ('Education', 'Education'),
        ('Health', 'Health'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='campaign_images/')
    deadline = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)
    category_id = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending Approval')
    fundraiser = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='campaigns', on_delete=models.CASCADE)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'campaign'

    def __str__(self):
        return self.title


from django.utils import timezone

class CampaignApprovalHistory(models.Model):
    ACTION_CHOICES = [
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='approval_history')
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='admin_approvals')
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Campaign Approval History'
        verbose_name_plural = 'Campaign Approval Histories'

    def __str__(self):
        return f'{self.campaign.title} - {self.action} by {self.admin.username}'



class Donation(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    stripe_payment_intent = models.CharField(max_length=255, blank=True, null=True)  # Stripe-specific field
    stripe_receipt_url = models.URLField(blank=True, null=True)  # For storing Stripe receipt URL

    def __str__(self):
        return f"Donation of {self.amount} to {self.campaign.title} by {self.donor.username}"



from django.db import models
from django.conf import settings

class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.recipient.username}"


from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name