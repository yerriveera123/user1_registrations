from django.shortcuts import render
from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from app.models import *
# Create your views here.
def registration(request):
    UFDO=UserForm()
    PFDO=ProfileForm()
    d={'UFDO':UFDO,'PFDO':PFDO}
    if request.method=='POST' and request.FILES:
        NMUFDO=UserForm(request.POST)
        NMPFDO=ProfileForm(request.POST,request.FILES)
        if NMUFDO.is_valid() and NMPFDO.is_valid():
            MFUDO=NMUFDO.save(commit=False)
            pw=NMUFDO.cleaned_data['password']
            MFUDO.set_password(pw)
            MFUDO.save()
            MPFDO=NMPFDO.save(commit=False)
            MPFDO.username=MFUDO
            MPFDO.save()

            send_mail('registration','thank you for registration','yerriveera@gmail.com',[MFUDO.email],fail_silently=False)
            return HttpResponse('registration is succeesfull')

        
        else:
            return HttpResponse('invalid data')



    return render(request,'registration.html',d)
def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')


def user_login(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('Invalid Credentials')
    return render(request,'user_login.html')
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
@login_required
def display_data(request):
    username=request.session['username']
    UO=User.objects.get(username)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}
    return render(request,'display_data.html',d)

