from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView, View, CreateView, ListView, UpdateView, DetailView, FormView
)
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.mail import send_mail
from django.views.generic import TemplateView

from hearthive_app.models import Fundraiser, Donor, Donation, Campaign, CampaignApprovalHistory, Notification
from .forms import (
    DonorModelForm, FundraiserModelForm, DonorUpdateForm, FundraiserUpdateForm,
    CampaignForm, DonationForm, ContactForm
)





class HomePageView(ListView):
    model = Campaign
    template_name = 'home.html'
    context_object_name = 'campaigns'

    def get_queryset(self):
        return Campaign.objects.filter(status='Active')




class DonorRegisterView(CreateView):
    form_class = DonorModelForm
    template_name = 'donor_register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])  
        user.save()
        send_mail(
            'Welcome to HeartHive as a Donor!',
            f'Hi {user.first_name},\n\nThank you for registering as a donor on our platform.',
            'kashifnoor789789@gmail.com',  
            [user.email],   
            fail_silently=False,
        )

        return super().form_valid(form)
    
    

class FundraiserRegisterView(CreateView):
    form_class = FundraiserModelForm
    template_name = 'fundraiser_register.html'
    success_url = reverse_lazy('login') 

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password']) 
        user.save()  
        send_mail(
            'Welcome to HeartHive as a Fundraiser!',
            f'Hi {user.first_name},\n\nThank you for registering as a fundraiser on our platform.',
            'kashifnoor789789@gmail.com',  
            [user.email],   
            fail_silently=False,
        )

        return super().form_valid(form)



class AdminPortalView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Campaign
    template_name = 'admin_portal.html'
    context_object_name = 'campaigns'

    def get_queryset(self):
        return Campaign.objects.filter(status='Pending Approval')

    def test_func(self):
        return self.request.user.is_superuser




class FundraiserPortalView(TemplateView):
    template_name = 'fundraiser_portal.html'




class DonorPortalView(TemplateView):
    template_name = 'donor_portal.html'



class CustomLoginView(LoginView):
    template_name = 'login.html'
    
    def get_success_url(self):
        user = self.request.user

        if user.is_superuser:
            return reverse_lazy('admin_portal')
        
      
        elif hasattr(user, 'fundraiser'):
            return reverse_lazy('fundraiser_portal')
        

        elif hasattr(user, 'donor'):
            return reverse_lazy('donor_portal')
    
        return reverse_lazy('home')
    



class FundraiserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'fundraiser_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fundraiser = get_object_or_404(Fundraiser, id=self.request.user.id)
        context['fundraiser'] = fundraiser 
        return context



class FundraiserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Fundraiser
    form_class = FundraiserUpdateForm
    template_name = 'fundraiser_profile_update.html'
    success_url = reverse_lazy('fundraiser_profile') 

    def get_object(self):
        return get_object_or_404(Fundraiser, id=self.request.user.id)




class DonorProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'donor_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        donor = get_object_or_404(Donor, id=self.request.user.id)
        context['donor'] = donor 

        donations = Donation.objects.filter(donor=donor).select_related('campaign').order_by('-date')
        context['donations'] = donations 
        return context




class DonorProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Donor
    form_class = DonorUpdateForm
    template_name = 'donor_profile_update.html'
    success_url = reverse_lazy('donor_profile')  

    def get_object(self):
        return get_object_or_404(Donor, id=self.request.user.id)

    

class FundraiserCampaignCreateView(LoginRequiredMixin, CreateView):
    model = Campaign
    form_class = CampaignForm
    template_name = 'create_campaign.html'
    success_url = reverse_lazy('fundraiser_portal')

    def form_valid(self, form):
        campaign = form.save(commit=False)
        campaign.fundraiser = self.request.user
        campaign.status = 'Pending Approval'  
        campaign.save()
        return super().form_valid(form)


class FundraiserCampaignListView(LoginRequiredMixin, ListView):
    model = Campaign
    template_name = 'campaign_list.html'
    context_object_name = 'campaigns'

    def get_queryset(self):
        return Campaign.objects.filter(fundraiser=self.request.user)




class AdminCampaignApprovalListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Campaign
    template_name = 'campaign_approval_list.html'
    context_object_name = 'pending_campaigns'

    def get_queryset(self):
        return Campaign.objects.filter(status='Pending Approval')

    def test_func(self):
        return self.request.user.is_superuser



class AdminCampaignApproveView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Campaign
    fields = ['status']  
    template_name = 'campaign_approve.html'
    success_url = reverse_lazy('admin_portal')  

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        form.instance.status = 'Active'  
        response = super().form_valid(form)
        
        print(f"Campaign '{form.instance.title}' has been approved by {self.request.user.username}")
        CampaignApprovalHistory.objects.create(
            campaign=form.instance,
            admin=self.request.user,
            action='Approved',  
            timestamp=timezone.now()
        )
        
        return response




class AdminApprovalHistoryView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = CampaignApprovalHistory
    template_name = 'admin_approval_history.html'
    context_object_name = 'approval_history'

    def test_func(self):
        return self.request.user.is_superuser





class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notifications.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by('-date_created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unread_notifications_count'] = Notification.objects.filter(
            recipient=self.request.user,
            is_read=False
        ).count()
        return context



class CampaignDetailView(DetailView):
    model = Campaign
    template_name = 'campaign_detail.html'
    context_object_name = 'campaign'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_donations = self.object.donation_set.aggregate(Sum('amount'))['amount__sum'] or 0
        context['total_donations'] = total_donations

        donations = self.object.donation_set.select_related('donor').order_by('-date')
        context['donations'] = donations  

        return context
    

from django.views.generic import DeleteView

class CampaignDeleteView(UserPassesTestMixin, DeleteView):
    model = Campaign
    template_name = 'campaign_confirm_delete.html'
    success_url = reverse_lazy('home')  # Redirect after deletion

    def test_func(self):
        campaign = self.get_object()
        return self.request.user == campaign.fundraiser



class CampaignOverviewView(DetailView):
    model = Campaign
    template_name = 'campaign_overview.html'
    context_object_name = 'campaign'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    




class AboutView(TemplateView):
    template_name = 'about.html'




class ContactUsView(FormView):
    template_name = 'contact_us.html'
    form_class = ContactForm
    success_url = reverse_lazy('home')  

    def form_valid(self, form):
        form.save()
        send_mail(
            subject='New Contact Us Message',
            message=f"Name: {form.cleaned_data['name']}\nEmail: {form.cleaned_data['email']}\nMessage: {form.cleaned_data['message']}",
            from_email='kashifnoor789789@gmail.com',  
            recipient_list=['kashifnoor789789@gmail.com'], 
        )       
        return super().form_valid(form)







from django.shortcuts import reverse
import stripe
from django.conf import settings
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Campaign, Donation

# Set Stripe secret key
stripe.api_key = settings.SECRET_KEY  # Ensure you use the correct Stripe secret key

class DonateView(LoginRequiredMixin, View):
    def get(self, request, campaign_id):
        campaign = Campaign.objects.get(id=campaign_id)
        return render(request, 'donation_payment.html', {
            'campaign': campaign,
            'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,
        })

    def post(self, request, campaign_id):
        campaign = Campaign.objects.get(id=campaign_id)
        amount_str = request.POST.get('amount')

        if not amount_str:
            return render(request, 'donation_payment.html', {
                'campaign': campaign,
                'error': "Please enter an amount."
            })

        try:
            # Convert to cents for Stripe
            amount_in_cents = int(float(amount_str) * 100)
        except ValueError:
            return render(request, 'donation_payment.html', {
                'campaign': campaign,
                'error': "Invalid amount entered."
            })

        try:
            # Create Stripe Checkout session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f"Donation for {campaign.title}",
                        },
                        'unit_amount': amount_in_cents,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri(reverse('donation_success')) + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=request.build_absolute_uri(reverse('home')),
                # success_url=request.build_absolute_uri('donation_success') + '?session_id={CHECKOUT_SESSION_ID}',
                # cancel_url=request.build_absolute_uri('/home/'),
                metadata={'campaign_id': campaign.id, 'donor_id': request.user.id},
            )

            # Track donation (before successful payment)
            Donation.objects.create(
                campaign=campaign,
                donor=request.user,
                amount=amount_str,
                stripe_payment_intent=session['id']  # Track with Stripe session ID
            )

            try:
                # Notify the superuser (assuming there is one)
                superuser = get_user_model().objects.get(is_superuser=True)
                Notification.objects.create(
                    recipient=superuser,
                    message=f"New donation of {amount_str} made to campaign '{campaign.title}' by {request.user.username}.",
                    is_read=False
                )
            except get_user_model().DoesNotExist:
                pass 

            # Notify the fundraiser
            Notification.objects.create(
                recipient=campaign.fundraiser,  
                message=f"Your campaign '{campaign.title}' received a new donation of {amount_str} from {request.user.username}.",
                is_read=False
            )

            return redirect(session.url, code=303)

        except stripe.error.StripeError as e:
            return render(request, 'donation_payment.html', {
                'campaign': campaign,
                'error': f"Stripe error: {str(e)}"
            })








class DonationSuccessView(View):
    def get(self, request):
        return render(request, 'payment_success.html')
