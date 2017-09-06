from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Guest(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	
	MAYBESEXA = (
		('b','Boy'),
		('g','Girl'),
		('s','Secret')
		)
	name = models.CharField(max_length=30)
	sex = models.CharField(max_length=1, choices=MAYBESEXA)
	phone = models.CharField(max_length=11, unique=True)
	MAYBESTATUSA = (
		('y','yes'),
		('n','no'),
		)
	status = models.CharField(max_length=1, choices=MAYBESTATUSA)

class Association(models.Model):
	AID = models.CharField(max_length=20, unique=True)
	name = models.CharField(max_length=20, unique=True)
	MAYBESTATUSB = (
		('y','yes'),
		('n','no'),
		)
	status = models.CharField(max_length=1, choices=MAYBESTATUSB)

class Manager(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	association = models.ForeignKey(Association, on_delete=models.CASCADE, null=True)
	MAYBETYPEC = (
		('s','shelian'),
		('l','zhidaolaoshi'),
		('z','zheliba'),
		)
	mtype = models.CharField(max_length=1, choices=MAYBETYPEC)

class Record(models.Model):
	guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
	MAYBEROMED = (
		('a','All'),
		('b','Big'),
		('x1','Xiao1'),
		('x2','Xiao2'),
		)
	room = models.CharField(max_length=2, choices=MAYBEROMED)
	MAYBESTATUSD = (
		('11','LDealing'),
		('12','SDealing'),
		('13','ZDealing'),
		('2','OK'),
		('31','LCancled'),
		('32','SCancled'),
		('33','ZCancled'),
		('4','Done'),
		)
	status = models.CharField(max_length=2, choices=MAYBESTATUSD)
	Lanswer = models.CharField(max_length=100, null = True)
	Sanswer = models.CharField(max_length=100, null = True)
	Zanswer = models.CharField(max_length=100, null = True)
	MAYBETYPED = (
		('n','normal'),
		('s','shetuan'),
		)
	rtype = models.CharField(max_length=1,choices=MAYBETYPED)
	association = models.ForeignKey(Association, null = True)
	reason = models.CharField(max_length=100, null = True)
	up_time = models.DateTimeField(auto_now=True)
	day_time = models.DateField(null = True)
	start_time = models.IntegerField(null = True)
	end_time = models.IntegerField(null = True)

class Bad_record(models.Model):
	record = models.ForeignKey(Record, on_delete=models.CASCADE)
	punish_time = models.DateTimeField(null = True)
