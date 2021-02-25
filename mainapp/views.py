from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


import warnings

from django.conf import settings
#from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, QueryDict
from django.template.response import TemplateResponse
#from django.utils.deprecation import RemovedInDjango20Warning
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.utils.translation import ugettext as _
#from django.utils.six.moves.urllib.parse import urlparse, urlunparse
from django.shortcuts import resolve_url
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import (REDIRECT_FIELD_NAME, login as auth_login,
    logout as auth_logout, get_user_model, update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import  PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site



def home(request):
    return render(request,"mainapp/home.html")

def joblist(request):
    return render(request,"mainapp/joblist.html")

def aplyjob(request):
    return render(request,"mainapp/aplyjob.html")


#registraion
def profile(request):
    return render(request,"registration/profile.html")

def login(request):
    return render(request,"registration/login.html") 

def passreset(request):
    return render(request,"registration/passreset.html") 

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
               # messages.info(request, 'Username has been taken')
                return redirect('login')
            elif User.objects.filter(email=email).exists():
                #messages.info(request, 'Email already exists')
                return redirect('login')
            else:
                user = User.objects.create_user(username=username,email=email,password=password1)
                user.save()
                #messages.success(request, 'Congrats for signing up!')
                return redirect('login')
        else:
           # messages.info(request, 'password does not match')
            return redirect('login')

    else:
        return render(request,'registration/register.html',{'title':'register'})



@csrf_protect
def password_reset(request, is_admin_site=False,
                   template_name='registration/password_reset_form.html',
                   email_template_name='registration/password_reset_email.html',
                   subject_template_name='registration/password_reset_subject.txt',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email=None,
                   current_app=None,
                   extra_context=None,
                   html_email_template_name=None):
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_done')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
                'html_email_template_name': html_email_template_name,
            }
            if is_admin_site:
                warnings.warn(
                    "The is_admin_site argument to "
                    "django.contrib.auth.views.password_reset() is deprecated "
                    "and will be removed in Django 2.0.",
                    RemovedInDjango20Warning, 3
                )
                opts = dict(opts, domain_override=request.get_host())
            form.save(**opts)
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = password_reset_form()
    context = {
        'form': form,
        'title': _('Password reset'),
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)
