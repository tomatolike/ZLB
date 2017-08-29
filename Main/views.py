from django.shortcuts import render, redirect, reverse, render_to_response
from .models import *
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist
import math
import operator


# Create your views here.

def login(request):
    return render(request, 'login.html')

def register(request):
	if request.method == 'GET':
		return render(request, 'register.html')
	else :
		if 'username' in request.POST:
			userid = request.POST['username']
			if User.objects.filter(username = userid).exists():
				return HttpResponse('<script>alert("该学号已经注册了哦！");location.replace("/Main/register/");</script>')
		else :
			return HttpResponse('<script>alert("请输入学号！");location.replace("/Main/register/");</script>')
		if 'password' in request.POST:
			userps = request.POST['password']
			if 'password2' in request.POST:
				userps2 = request.POST['password2']
				if userps2 != userps:
					return HttpResponse('<script>alert("两次密码输入不一致哦！");location.replace("/Main/register/");</script>')
			else :
				return HttpResponse('<script>alert("请输入确认密码！");location.replace("/Main/register/");</script>')
			if len(userps)<8 or len(userps)>20:
				return HttpResponse('<script>alert("密码长度不正确哦！");location.replace("/Main/register/");</script>')
		else :
			return HttpResponse('<script>alert("请输入密码！");location.replace("/Main/register/");</script>')
		if 'name' in request.POST:
			userna = request.POST['name']
			if len(userna)>30:
				return HttpResponse('<script>alert("请输入30个字内的姓名！");location.replace("/Main/register/");</script>')
		else :
			return HttpResponse('<script>alert("请输入姓名！");location.replace("/Main/register/");</script>')
		if 'phone' in request.POST:
			userph = request.POST['phone']
			if len(userph)!=11:
				return HttpResponse('<script>alert("手机号码长度不正确！");location.replace("/Main/register/");</script>')
		else :
			return HttpResponse('<script>alert("请输入手机号码！");location.replace("/Main/register/");</script>')
		if 'mail' in request.POST:
			usermail = request.POST['mail']
		else :
			return HttpResponse('<script>alert("请输入电子邮箱！");location.replace("/Main/register/");</script>')
		if 'sex' in request.POST:
			usersex = request.POST['sex']
		else :
			usersex = 's'

		user = User()
		user.username = userid
		user.set_password(userps)
		user.email = usermail
		user.save()

		newguest = Guest()
		newguest.user = user
		newguest.name = userna
		newguest.sex = usersex
		newguest.phone = userph
		newguest.status = 'y'
		newguest.save()

		return HttpResponse('<script>alert("注册成功！请登录！");location.replace("/Main/login/");</script>')

def logIn(request):
	uname = request.POST['username']
	pword = request.POST['password']
	logtype = request.POST['ty']
	if uname is None or pword is None:
		return HttpResponse('<script>alert("请输入用户名和密码！");location.replace("/Main/login/");</script>')
	user = authenticate(username=uname, password=pword)
	#user1 = User.objects.filter(username=uname)
	#user2 = User.objects.filter(password=pword)
	if user is None:
		return HttpResponse('<script>alert("密码或用户名错误！");location.replace("/Main/login/");</script>')
	if logtype == 'A':
		try:
			test = user.guest
		except:
			return HttpResponse('<script>alert("密码或用户名错误!！");location.replace("/Main/login/");</script>')
	if logtype == 'M':
		try:
			test = user.manager
		except:
			return HttpResponse('<script>alert("密码或用户名错误!！");location.replace("/Main/login/");</script>')
	auth.login(request=request, user=user)
	if logtype == 'A':
		return HttpResponse('<script>alert("登陆成功！");location.replace("/Apply/myinfo/");</script>')
	elif logtype == 'M':
		return HttpResponse('<script>alert("登陆成功！");location.replace("/Manage/myinfo/");</script>')

