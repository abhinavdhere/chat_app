from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from .models import message
#from .forms import PostForm
from .forms import MyRegistrationForm
from django.template.context_processors import csrf
from django.contrib import auth
from django.http import HttpResponseRedirect

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
	return render(request,'users/login.html',c)

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