from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.utils import timezone

# Create your models here.


class User(AbstractUser):
    # abstract user has username (we are going to us email) first and last name
    userTypes = (
        ('A', 'Admin'),
        ('C', 'Counter'),
        ('G', 'Guest'),
    )
    role = models.CharField(max_length=1, choices=userTypes, default="A")

    def __str__(self):
        return self.username


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Space(models.Model):
    name = models.CharField(max_length=255, unique=True)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Employee(models.Model):

    genderTypes = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    name = models.CharField(max_length=255, unique=True)
    gender = models.CharField(max_length=1, choices=genderTypes, null=True, blank=True)
    hiring_date = models.DateField(null=True, blank=True)
    leaving_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    fixed_salary = models.FloatField()
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Motivation(models.Model):
    motivationTypes = (
        ('R', 'Reward'),
        ('C', 'Cutoff'),
        ('L', 'Loan'),
    )

    amount = models.FloatField(default=0)
    type = models.CharField(max_length=1, choices=motivationTypes)
    date = models.DateField(default=timezone.now)
    notes = models.TextField(null=True, blank=True)
    isActive = models.BooleanField(default=True)

    employee = models.ForeignKey(Employee, related_name='motivations', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.employee.name)


class Ratio(models.Model):
    employee = models.ForeignKey(Employee, related_name='ratios', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='ratios', on_delete=models.CASCADE)
    space = models.ForeignKey(Space, related_name='ratios', on_delete=models.DO_NOTHING, null=True, blank=True)

    ratio = models.FloatField(default=0.0)
    thresh = models.FloatField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.employee.name + ", " + self.project.name + ", " + str(self.ratio)


class Client(models.Model):
    name = models.CharField(max_length=255, unique=True)
    ceo_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    fax = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    work_field = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(null=True, blank=True)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    from_date = models.DateField(datetime.now())
    to_date = models.DateField()
    amount = models.FloatField(default=0)
    paper_id = models.IntegerField(unique=True)
    notes = models.TextField(null=True, blank=True)
    isActive = models.BooleanField(default=True)

    project = models.ForeignKey(Project, related_name='subscriptions', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name='subscriptions', on_delete=models.CASCADE)
    employees = models.ManyToManyField(Employee)
    owner = models.ForeignKey(Employee, related_name='subscriptions', on_delete=models.DO_NOTHING, blank=True, null=True)
    spaces = models.ManyToManyField(Space)

    def __str__(self):
        return str(self.client.name)


class Payment(models.Model):
    amount = models.FloatField(default=0)
    paper_id = models.IntegerField(unique=True)
    date = models.DateField(default=timezone.now)
    notes = models.TextField(null=True, blank=True)
    isActive = models.BooleanField(default=True)

    subscription = models.ForeignKey(Subscription, related_name='payments', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.amount)


class Transaction(models.Model):
    transactionType = (
        ('I', 'Income'),
        ('O', 'Outcome'),
    )

    amount = models.FloatField(default=0)
    type = models.CharField(max_length=1, choices=transactionType)
    date = models.DateField(datetime.now())
    notes = models.TextField(null=True, blank=True)
    isActive = models.BooleanField(default=True)

