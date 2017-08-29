from django.shortcuts import render, redirect, reverse, render_to_response
from .models import *
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError
from Main.models import Guest, Association, Manager, Record, Bad_record
from django.core.exceptions import ObjectDoesNotExist
import math
import operator

@login_required
def myinfo1(request):
	user = request.user
	guest = user.guest
	un = guest.name
	pn = guest.phone
	mb = user.email
	sx = guest.sex
	return render(request, 'myinfo1.html', {'username':user,'name':un,'phonenumber': pn,'mailbox':mb,'sex':sx})

@login_required
def modifyinfo(request):
	newname = request.POST['name']
	newphone = request.POST['phone']
	newmail = request.POST['mail']
	user = request.user
	guest = user.guest
	guest.name = newname
	guest.phone = newphone
	user.email = newmail
	user.save()
	guest.save()
	return HttpResponse('<script>alert("修改成功！");location.replace("/Apply/myinfo/");</script>')

@login_required
def modifycode(request):
	user = request.user
	uname = user.username
	gs = user.guest
	nm = gs.name
	if request.method == 'POST':
		old = request.POST['ori']
		new1 = request.POST['newcode']
		new2 = request.POST['newcode2']
		if old is None or new1 is None or new2 is None:
			return HttpResponse('<script>alert("请输入完整信息！");location.replace("/Apply/modifycode/");</script>')
		u = authenticate(username=uname, password=old)
		if u is None:
			return HttpResponse('<script>alert("原密码错误！");location.replace("/Apply/modifycode/");</script>')
		if len(new1)<8 or len(new2)>20:
			return HttpResponse('<script>alert("新密码长度不正确！");location.replace("/Apply/modifycode/");</script>')
		if new1 == old:
			return HttpResponse('<script>alert("新密码与原密码不得一样！");location.replace("/Apply/modifycode/");</script>')
		if new1 != new2:
			return HttpResponse('<script>alert("新密码重复输入不正确！");location.replace("/Apply/modifycode/");</script>')
		user.set_password(new1)
		user.save()
		gs.save()
		auth.login(request=request, user=user)
		return HttpResponse('<script>alert("修改成功！");location.replace("/Apply/myinfo/");</script>')
	else:
		return render(request, 'myinfo2.html', {'name':nm})

@login_required
def myrecord(request):
	user = request.user
	gs = user.guest
	nm = gs.name
	try:
		recordlist = Record.objects.get(guest = gs)
	except ObjectDoesNotExist:
		recordlist = None
	return render(request, 'myinfo3.html', {'name':nm,'allrecord_list':recordlist})

@login_required
def infoquery(request):
	user = request.user
	gs = user.guest
	nm = gs.name
	return render(request, 'myinfo4-0.html', {'name':nm})

@login_required
def QCquery(request):
	user = request.user
	gs = user.guest
	nm = gs.name
	return render(request, 'myinfo4-1.html', {'name':nm})
