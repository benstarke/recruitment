from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    
    #pages
    path("",views.home, name="home" ),
    path("joblist/",views.joblist, name="joblist" ),
    path("aplyjob/",views.aplyjob, name="aplyjob"),
    
    #registration
    path("login/",views.login, name="login"),
    path("passreset/",views.passreset, name="passreset"),
    path("register/",views.register, name="register"),
    path("profile/",views.profile, name="profile"),

    #login
    #emails
    path('accounts/',include('django.contrib.auth.urls')),

    
]