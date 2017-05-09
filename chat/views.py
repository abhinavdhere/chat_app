from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from .models import message
#from .forms import PostForm
from .forms import MyRegistrationForm, MessageForm
from django.template.context_processors import csrf
from django.contrib import auth
from django.http import HttpResponseRedirect
from itertools import chain
from django.urls import reverse

def index(request):
    if not request.user.is_authenticated():
        return render(request,'chat/index.html')
    else:
        return HttpResponseRedirect('/home/')

def home(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')
    else:
        users = auth.models.User.objects.all()
        return render(request, 'chat/home.html' , {'user_obj':request.user,'users':users})

def login(request):
    c = {}
    c.update(csrf(request))
    return render(request,'chat/login.html',c)

def auth_view(request):
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = auth.authenticate(username=username,password=password)

    if user is not None:
        auth.login(request,user)
        return HttpResponseRedirect('/home')
    else:
        return HttpResponseRedirect('/invalid')

def invalid_login(request):
    return render(request, 'chat/invalid_login.html')

def logout(request):
    auth.logout(request)
    return render(request, 'chat/logout.html')

def register_user(request):
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)
        print ("got form")
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/register_success')
        else:
            print (form.errors)
    args = {}
    args.update(csrf(request))
    args['form']=MyRegistrationForm()
    print (args)
    return render(request,'chat/register.html',args)

def register_success(request):
    return render(request,'chat/register_success.html')

def chat_window(request,pk):
    receiver = get_object_or_404(auth.models.User, pk=pk)
    messages_r = message.objects.filter(recipient__id=request.user.pk, author__id=pk)
    messages_s = message.objects.filter(author__id=request.user.pk, recipient__id=pk)
    messages_all = sorted(chain(messages_r,messages_s),key=lambda message:message.timestamp)
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            messageToSend = form.save(commit=False)
            messageToSend.author = request.user
            messageToSend.recipient = receiver
            messageToSend.timestamp = timezone.now()
            messageToSend.save()
            return HttpResponseRedirect("/chat_window/"+str(pk))
    else:
        form = MessageForm()
    return render(request,'chat/chat_window.html',{'receiver':receiver,'messages_all':messages_all,'form':form})