from datetime import timezone
from distutils.command.upload import upload
from email.mime import image
import numbers
from pyexpat import model
from ssl import Options
from tabnanny import check
from tkinter import CASCADE

from unicodedata import category, name
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse_lazy

# Create your models here.


class RoomCategory(models.Model):
    category = models.CharField(max_length=50)
    rate = models.FloatField()

    def __str__(self):
        return self.category


class Room(models.Model):

    ROOM_CATEGORIES = (
        ('Ac-Single', 'Ac-Single'),
        ('Single', 'Single'),
        ('Deluex', 'Deluex'),
        ('King', 'King'),
        ('Queen', 'Queen'),
        ('Stduio', 'Stduio'),
        ('Hollywood-Twin-Room', 'Hollywood-Twin-Room'),
        ('Executive', 'Executive'),
        ('MiniSuite', 'MiniSuite'),
        ('PresidentialSuite', 'PresidentialSuite'),
        ('Apartments', 'Apartments'),
        ('ConnectingRooms', 'ConnectingRooms'),
        ('MurphyRooms', 'MurphyRooms'),
        ('Accessible', 'Accessible'),
        ('Cabana', 'Cabana'),
        ('Adjoining Rooms', 'AdjoiningRoom'),
        ('Villa', 'Villa'),
        ('ExecutiveRoom', 'ExecutiveRoom'),
        ('Non-SmokingRoom', 'Non-SmokingRoom'),

    )
   # number = models.ForeignKey(RoomNumber, on_delete=CASCADE, unique=True, blank=True, null=True)

    #number = models.IntegerField()
    category = models.CharField(max_length=50, choices=ROOM_CATEGORIES)
    beds = models.IntegerField()
    desc = models.TextField()
    capacity = models.IntegerField()
    image = models.CharField(max_length=10000)
    price = models.IntegerField()

    def __str__(self):
        return f'{self.category} with {self.beds} beds for {self.capacity} people'


class RoomNumber(models.Model):
    room_number = models.IntegerField(unique=True)
    category = models.ForeignKey(
        Room, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.room_number)


class BookingRoom(models.Model):

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    room = models.ForeignKey(RoomNumber, on_delete=models.CASCADE,  null=True)
    check_in = models.DateField()
    check_out = models.DateField()
    total_bill = models.IntegerField(null=True, blank=True)
    status = models.BooleanField(default=False)

    def bill(self):
        days = self.check_out-self.check_in
        day = str(days).split(" ", 1)[0]
        total_bill = self.room.category.price * int(day)
        return total_bill
        # return day

    def __str__(self):
        return f'From = {self.check_in.strftime("%d-%b-%Y %H:%M")} To = {self.check_out.strftime("%d-%b-%Y %H:%M")}'


sex_choice = (
    ('Male', 'Male'),
    ('Female', 'Female')
)


class UserProfiles(models.Model):
    user = models.CharField(max_length=50, blank=True, null=True)
    FirstName = models.CharField(max_length=50, blank=True)
    LastName = models.CharField(max_length=50, blank=True)
    DateofBirth = models.DateField(blank=True, null=True)
    Email = models.EmailField(blank=True)
    gender = models.CharField(
        max_length=50, choices=sex_choice, default='Male')
    is_staff = models.BooleanField(default=False)
    need_approve = models.BooleanField(default=True)

    def __str__(self):
        return self.user


class ContactUs(models.Model):
    name = models.CharField(max_length=15)
    email = models.CharField(max_length=30)
    phone = models.CharField(max_length=11)
    message = models.CharField(max_length=200)


class Staff(models.Model):
    name = models.ForeignKey(UserProfiles, on_delete=models.CASCADE)

    def __str__(self):
        return self.name.user


class StaffTask(models.Model):

    user = models.ForeignKey(Staff, on_delete=models.CASCADE)
    task = models.CharField(max_length=200)
    room = models.ForeignKey(RoomNumber, on_delete=models.CASCADE)
    assigned = models.DateField()
    deadline = models.DateField()
    complete = models.BooleanField(default=False)


class payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Name_On_Card = models.CharField(max_length=50)
    Credit_Card_Number = models.CharField(max_length=12)
    Exp_Month = models.CharField(max_length=2)
    Exp_Year = models.CharField(max_length=4)
    CVV = models.CharField(max_length=3)
