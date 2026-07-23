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



def index(request):
    services = Service.objects.all()
    return render(request, 'index.html', {
        'services': services
    })
def home(request):
    return render(request, "base.html")

def about(request):
    return render(request, "about.html")


def client(request):
    return render(request, "client.html")



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



def contact(request):
    if request.method == 'POST':
        user_name = request.POST.get('name')
        user_email = request.POST.get('email')
        email_subject = request.POST.get('subject')
        user_message = request.POST.get('message')

        full_subject = f"New Inquiry: {email_subject}"
        full_body_message = f"You received a new contact form submission:\n\n" \
                            f"Name: {user_name}\n" \
                            f"Email: {user_email}\n\n" \
                            f"Message:\n{user_message}"

        try:
            # Django core mailing module trigger
            send_mail(
                subject=full_subject,
                message=full_body_message,
                from_email=settings.EMAIL_HOST_USER,  
                recipient_list=['syslink26@gmail.com'],  
                fail_silently=False,
            )
            messages.success(request, "Your message has been dispatched successfully!")
        except Exception as e:
            messages.error(request, f"Error sending message: {e}. Please try again later.")
        
        return redirect('contact')  

    return render(request, 'contact.html')