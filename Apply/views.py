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
from datetime import datetime, time
from django.utils.timezone import now, timedelta
import time
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
	res = [[0 for i in range(6)] for j in range(6)]

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
	now_day = now().date()
	wk_day = now_day.weekday()
	if wk_day == 0:
		start = now_day + timedelta(days = 7)
	elif wk_day == 1:
		start = now_day + timedelta(days = 6)
	elif wk_day == 2:
		start = now_day + timedelta(days = 5)
	elif wk_day == 3:
		start = now_day + timedelta(days = 4)
	elif wk_day == 4:
		start = now_day + timedelta(days = 3)
	elif wk_day == 5:
		start = now_day + timedelta(days = 2)
	else :
		start = now_day + timedelta(days = 1)

	ans = [[0 for i in range(28)] for j in range(13)]
	ot = 10
	zt = ot
	count = 0

	week1=[[0 for i in range(7)] for j in range(13)]
	wek1 = []
	for i in range(7):
		wek1.append(start + timedelta(days = i))

	week2=[[0 for i in range(7)] for j in range(13)]
	wek2 = []
	for i in range(7):
		wek2.append(start + timedelta(days = i+7))

	week3=[[0 for i in range(7)] for j in range(13)]
	wek3 = []
	for i in range(7):
		wek3.append(start + timedelta(days = i+14))

	week4=[[0 for i in range(7)] for j in range(13)]
	wek4 = []
	for i in range(7):
		wek4.append(start + timedelta(days = i+21))

	aday=[]
	for k in range(13):
		aday.append(k)

	aweek=[]
	for k in range(7):
		aweek.append(k)

	for day in range(28):
		to_day = start + timedelta(days = day)
		records = Record.objects.filter(day_time = to_day, room = 'a')
		for r in records:
			if r.status == '2':
				st = r.start_time
				st = st - zt
				et = r.end_time
				et = et - zt
				for t in range(st, et):
					ans[t][day] = 2
			elif r.status == '11' or r.status == '12' or r.status == '13':
				st = r.start_time
				st = st - zt
				et = r.end_time
				et = et - zt
				for t in range(st, et):
					ans[t][day] = 1
			else :
				count = count + 1
	for t in range(13):
		for day in range(7):
			week1[t][day] = ans[t][day]
		for day in range(7,14):
			week2[t][day-7] = ans[t][day]
		for day in range(14,21):
			week3[t][day-14] = ans[t][day]
		for day in range(21,28):
			week4[t][day-21] = ans[t][day]
	return render(request, 'myinfo4-1.html', {'name':nm,'res':ans,'wek1':wek1,'week1':week1,'wek2':wek2,'week2':week2,'wek3':wek3,'week3':week3,'wek4':wek4,'week4':week4,'aday':aday,'aweek':aweek})

@login_required
def HYSquery(request):
	user = request.user
	gs = user.guest
	nm = gs.name
	now_day = now().date()
	wk_day = now_day.weekday()
	if wk_day == 0:
		start = now_day + timedelta(days = 7)
	elif wk_day == 1:
		start = now_day + timedelta(days = 6)
	elif wk_day == 2:
		start = now_day + timedelta(days = 5)
	elif wk_day == 3:
		start = now_day + timedelta(days = 4)
	elif wk_day == 4:
		start = now_day + timedelta(days = 3)
	elif wk_day == 5:
		start = now_day + timedelta(days = 2)
	else :
		start = now_day + timedelta(days = 1)

	ans = [[0 for i in range(28)] for j in range(13)]
	ot = 10
	zt = ot
	count = 0

	week1=[[0 for i in range(7)] for j in range(13)]
	wek1 = []
	for i in range(7):
		wek1.append(start + timedelta(days = i))

	week2=[[0 for i in range(7)] for j in range(13)]
	wek2 = []
	for i in range(7):
		wek2.append(start + timedelta(days = i+7))

	week3=[[0 for i in range(7)] for j in range(13)]
	wek3 = []
	for i in range(7):
		wek3.append(start + timedelta(days = i+14))

	week4=[[0 for i in range(7)] for j in range(13)]
	wek4 = []
	for i in range(7):
		wek4.append(start + timedelta(days = i+21))

	aday=[]
	for k in range(13):
		aday.append(k)

	aweek=[]
	for k in range(7):
		aweek.append(k)

	for day in range(28):
		to_day = start + timedelta(days = day)
		records = Record.objects.filter(day_time = to_day, room = 'b')
		for r in records:
			if r.status == '2':
				st = r.start_time
				st = st - zt
				et = r.end_time
				et = et - zt
				for t in range(st, et):
					ans[t][day] = 2
			elif r.status == '11' or r.status == '12' or r.status == '13':
				st = r.start_time
				st = st - zt
				et = r.end_time
				et = et - zt
				for t in range(st, et):
					ans[t][day] = 1
			else :
				count = count + 1
	for t in range(13):
		for day in range(7):
			week1[t][day] = ans[t][day]
		for day in range(7,14):
			week2[t][day-7] = ans[t][day]
		for day in range(14,21):
			week3[t][day-14] = ans[t][day]
		for day in range(21,28):
			week4[t][day-21] = ans[t][day]
	return render(request, 'myinfo4-2.html', {'name':nm,'res':ans,'wek1':wek1,'week1':week1,'wek2':wek2,'week2':week2,'wek3':wek3,'week3':week3,'wek4':wek4,'week4':week4,'aday':aday,'aweek':aweek})

@login_required
def XB1query(request):
	user = request.user
	gs = user.guest
	nm = gs.name
	now_day = now().date()
	wk_day = now_day.weekday()
	if wk_day == 0:
		start = now_day + timedelta(days = 7)
	elif wk_day == 1:
		start = now_day + timedelta(days = 6)
	elif wk_day == 2:
		start = now_day + timedelta(days = 5)
	elif wk_day == 3:
		start = now_day + timedelta(days = 4)
	elif wk_day == 4:
		start = now_day + timedelta(days = 3)
	elif wk_day == 5:
		start = now_day + timedelta(days = 2)
	else :
		start = now_day + timedelta(days = 1)

	ans = [[0 for i in range(28)] for j in range(13)]
	ot = 10
	zt = ot
	count = 0

	week1=[[0 for i in range(7)] for j in range(13)]
	wek1 = []
	for i in range(7):
		wek1.append(start + timedelta(days = i))

	week2=[[0 for i in range(7)] for j in range(13)]
	wek2 = []
	for i in range(7):
		wek2.append(start + timedelta(days = i+7))

	week3=[[0 for i in range(7)] for j in range(13)]
	wek3 = []
	for i in range(7):
		wek3.append(start + timedelta(days = i+14))

	week4=[[0 for i in range(7)] for j in range(13)]
	wek4 = []
	for i in range(7):
		wek4.append(start + timedelta(days = i+21))

	aday=[]
	for k in range(13):
		aday.append(k)

	aweek=[]
	for k in range(7):
		aweek.append(k)

	for day in range(28):
		to_day = start + timedelta(days = day)
		records = Record.objects.filter(day_time = to_day, room = 'x1')
		for r in records:
			if r.status == '2':
				st = r.start_time
				st = st - zt
				et = r.end_time
				et = et - zt
				for t in range(st, et):
					ans[t][day] = 2
			elif r.status == '11' or r.status == '12' or r.status == '13':
				st = r.start_time
				st = st - zt
				et = r.end_time
				et = et - zt
				for t in range(st, et):
					ans[t][day] = 1
			else :
				count = count + 1
	for t in range(13):
		for day in range(7):
			week1[t][day] = ans[t][day]
		for day in range(7,14):
			week2[t][day-7] = ans[t][day]
		for day in range(14,21):
			week3[t][day-14] = ans[t][day]
		for day in range(21,28):
			week4[t][day-21] = ans[t][day]
	return render(request, 'myinfo4-3.html', {'name':nm,'res':ans,'wek1':wek1,'week1':week1,'wek2':wek2,'week2':week2,'wek3':wek3,'week3':week3,'wek4':wek4,'week4':week4,'aday':aday,'aweek':aweek})

@login_required
def XB2query(request):
	user = request.user
	gs = user.guest
	nm = gs.name
	now_day = now().date()
	wk_day = now_day.weekday()
	if wk_day == 0:
		start = now_day + timedelta(days = 7)
	elif wk_day == 1:
		start = now_day + timedelta(days = 6)
	elif wk_day == 2:
		start = now_day + timedelta(days = 5)
	elif wk_day == 3:
		start = now_day + timedelta(days = 4)
	elif wk_day == 4:
		start = now_day + timedelta(days = 3)
	elif wk_day == 5:
		start = now_day + timedelta(days = 2)
	else :
		start = now_day + timedelta(days = 1)

	ans = [[0 for i in range(28)] for j in range(13)]
	ot = 10
	zt = ot
	count = 0

	week1=[[0 for i in range(7)] for j in range(13)]
	wek1 = []
	for i in range(7):
		wek1.append(start + timedelta(days = i))

	week2=[[0 for i in range(7)] for j in range(13)]
	wek2 = []
	for i in range(7):
		wek2.append(start + timedelta(days = i+7))

	week3=[[0 for i in range(7)] for j in range(13)]
	wek3 = []
	for i in range(7):
		wek3.append(start + timedelta(days = i+14))

	week4=[[0 for i in range(7)] for j in range(13)]
	wek4 = []
	for i in range(7):
		wek4.append(start + timedelta(days = i+21))

	aday=[]
	for k in range(13):
		aday.append(k)

	aweek=[]
	for k in range(7):
		aweek.append(k)

	for day in range(28):
		to_day = start + timedelta(days = day)
		records = Record.objects.filter(day_time = to_day, room = 'x2')
		for r in records:
			if r.status == '2':
				st = r.start_time
				st = st - zt
				et = r.end_time
				et = et - zt
				for t in range(st, et):
					ans[t][day] = 2
			elif r.status == '11' or r.status == '12' or r.status == '13':
				st = r.start_time
				st = st - zt
				et = r.end_time
				et = et - zt
				for t in range(st, et):
					ans[t][day] = 1
			else :
				count = count + 1
	for t in range(13):
		for day in range(7):
			week1[t][day] = ans[t][day]
		for day in range(7,14):
			week2[t][day-7] = ans[t][day]
		for day in range(14,21):
			week3[t][day-14] = ans[t][day]
		for day in range(21,28):
			week4[t][day-21] = ans[t][day]
	return render(request, 'myinfo4-4.html', {'name':nm,'res':ans,'wek1':wek1,'week1':week1,'wek2':wek2,'week2':week2,'wek3':wek3,'week3':week3,'wek4':wek4,'week4':week4,'aday':aday,'aweek':aweek})

