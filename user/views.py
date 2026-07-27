from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import *

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import logging



def index(request):
    services = Service.objects.all()
    return render(request, 'index.html', {
        'services': services
    })
def home(request):
    return render(request, "base.html")

def about(request):
    return render(request, "about.html")


def partner(request):
    return render(request, "partner.html")



def services(request):
    categories = Category.objects.all()

    category_slug = request.GET.get('category')

    if category_slug:
        services = Service.objects.filter(category__slug=category_slug)
    else:
        services = Service.objects.all()

    return render(request, 'services.html', {
        'categories': categories,
        'services': services,
        'selected_category': category_slug,
    })


from django.shortcuts import render, get_object_or_404
from django.apps import apps 

def detail(request, service_id):
    Service_Model = apps.get_model('user', 'Service') 
    service = get_object_or_404(Service_Model, id=service_id)
    context = {
        'service': service
    }
    return render(request, "detail.html", context)




logger = logging.getLogger(__name__)

def contact(request):
    if request.method == 'POST':
        user_name = request.POST.get('name', '').strip()
        user_email = request.POST.get('email', '').strip()
        raw_subject = request.POST.get('subject', '').strip()
        email_subject = raw_subject.replace('\r', '').replace('\n', '')
        user_message = request.POST.get('message', '').strip()
        form_data = {
            'name': user_name,
            'email': user_email,
            'subject': raw_subject,
            'message': user_message,
        }
        if not user_name or not user_email or not user_message:
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'contact.html', {'form_data': form_data})

        full_subject = f"New Inquiry: {email_subject}"
        full_body_message = (
            f"You received a new contact form submission:\n\n"
            f"Name: {user_name}\n"
            f"Email: {user_email}\n\n"
            f"Message:\n{user_message}"
        )

        try:
            send_mail(
                subject=full_subject,
                message=full_body_message,
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', settings.EMAIL_HOST_USER),
                recipient_list=['syslink26@gmail.com'],
                reply_to=[user_email],
                fail_silently=False,
            )
            messages.success(request, "Your message has been dispatched successfully!")
            return redirect('contact') 
        except Exception as e:
            logger.error("Failed to send contact email: %s", e, exc_info=True)
            messages.error(request, "Unable to send your message right now. Please try again later.")
            return render(request, 'contact.html', {'form_data': form_data})
        
    return render(request, 'contact.html')