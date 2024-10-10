from django.urls import path
from .views import ( DonorRegisterView, FundraiserRegisterView, LogoutView, HomePageView, CustomLoginView,
AdminPortalView, FundraiserPortalView, DonorPortalView, FundraiserProfileView,
FundraiserCampaignListView, FundraiserCampaignCreateView,  AdminCampaignApproveView,
DonorProfileView, DonorProfileUpdateView, FundraiserProfileUpdateView,
CampaignDetailView, AdminApprovalHistoryView, NotificationListView, CampaignOverviewView,
AboutView, ContactUsView, CampaignDeleteView, DonateView, DonationSuccessView)

from django.conf.urls.static import static
from django.conf import settings




urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('contact/', ContactUsView.as_view(), name='contact'),
    path('about/', AboutView.as_view(), name='about'),
    path('register/donor/', DonorRegisterView.as_view(), name='donor_register'),
    path('register/fundraiser/', FundraiserRegisterView.as_view(), name='fundraiser_register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'), 

    path('admin-portal/', AdminPortalView.as_view(), name='admin_portal'),
    path('fundraiser-portal/', FundraiserPortalView.as_view(), name='fundraiser_portal'),  
    path('donor-portal/', DonorPortalView.as_view(), name='donor_portal'),

    path('fundraiser/profile/', FundraiserProfileView.as_view(), name='fundraiser_profile'),
    path('fundraiser/profile/update/', FundraiserProfileUpdateView.as_view(), name='fundraiser_profile_update'),
    path('donor/profile/', DonorProfileView.as_view(), name='donor_profile'),
    path('donor/profile/update/', DonorProfileUpdateView.as_view(), name='donor_profile_update'),
    

    path('campaign/<int:pk>/', CampaignDetailView.as_view(), name='campaign_detail'),
    path('campaign/<int:pk>/delete/', CampaignDeleteView.as_view(), name='delete_campaign'),


    path('create/', FundraiserCampaignCreateView.as_view(), name='create_campaign'),
    path('fundraiser/campaigns/', FundraiserCampaignListView.as_view(), name='fundraiser_portal'),


    path('custom_admin/campaigns/', AdminPortalView.as_view(), name='admin_portal'),  
    path('custom_admin/campaigns/approve/<int:pk>/', AdminCampaignApproveView.as_view(), name='admin_campaign_approve'),
    path('dashboard/approval-history/', AdminApprovalHistoryView.as_view(), name='admin_approval_history'),
    path('notifications/', NotificationListView.as_view(), name='notifications'),
    path('campaigns/<int:pk>/details/', CampaignOverviewView.as_view(), name='campaign_overview'),



    path('donate/<int:campaign_id>/', DonateView.as_view(), name='donate'),
    path('donation-success/', DonationSuccessView.as_view(), name='donation_success'),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)