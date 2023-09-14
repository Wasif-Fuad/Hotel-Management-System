from .models import RoomCategory, BookingRoom, Room, RoomNumber, payment
from .models import ContactUs, UserProfiles, StaffTask

from datetime import datetime
from atexit import register
from dataclasses import fields

from random import choices
from tkinter.tix import Form
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from django.core.exceptions import ValidationError
from .models import Room


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'password1', 'password2']


#  input_formats=["%Y-%m-%dT%H:%M", ],


class ContactForm(forms.ModelForm):

    class Meta:
        model = ContactUs
        fields = ('name', 'email', 'phone', 'message')


class BookingRoomForm(forms.ModelForm):

    class Meta:
        model = BookingRoom
        fields = '__all__'

        widgets = {'check_in': forms.DateInput(attrs={'placeholder': 'yyyy-mm-dd'}),
                   'check_out': forms.DateInput(attrs={'placeholder': 'yyyy-mm-dd'}),
                   'user': forms.Select(),
                   'room': forms.Select()



                   }


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfiles
        fields = ('user', 'FirstName', 'LastName',
                  'Email', 'DateofBirth', 'gender')

        widgets = {'user': forms.TextInput(attrs={'class': 'form-control'}),
                   'FirstName': forms.TextInput(attrs={'class': 'form-control'}),
                   'LastName': forms.TextInput(attrs={'class': 'form-control'}),
                   'Email': forms.EmailInput(attrs={'class': 'form-control'}),
                   'DateofBirth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                   'gender': forms.Select(attrs={'class': 'form-control'})


                   }


class StaffTaskForm(forms.ModelForm):
    class Meta:
        model = StaffTask
        fields = ('user', 'task', 'room', 'assigned', 'deadline')
        widgets = {'user': forms.Select(attrs={'class': 'form-control'}),
                   'task': forms.TextInput(attrs={'class': 'form-control'}),
                   'room': forms.Select(attrs={'class': 'form-control'}),
                   'assigned': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'yyyy-mm-dd', 'type': 'date'}),
                   'deadline': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'yyyy-mm-dd', 'type': 'date'}),



                   }


class CreateRoomform(forms.ModelForm):
    class Meta:
        model = RoomNumber
        fields = '__all__'
        widgets = {'Room_number': forms.NumberInput(attrs={'class': 'form-control'}),
                   'category': forms.Select(attrs={'class': 'form-control'}),




                   }


class CreateCategoryform(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        widgets = {'category': forms.Select(attrs={'class': 'form-control','id':'cate'}),
                   'beds': forms.NumberInput(attrs={'class': 'form-control','id':'beds'}),
                   'desc': forms.Textarea(attrs={'class': 'form-control','id':'detail'}),
                   'capacity': forms.NumberInput(attrs={'class': 'form-control','id':'capacity'}),
                   'image': forms.TextInput(attrs={'class': 'form-control', 'id':'image'}),
                   'price': forms.NumberInput(attrs={'class': 'form-control','id':'price'}),
                   }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = payment
        fields = ('Name_On_Card', 'Credit_Card_Number',
                  'Exp_Month', 'Exp_Year', 'CVV')

        widgets = {'Name_On_Card': forms.TextInput(attrs={'class': 'form-control'}),
                   'Credit_Card_Number': forms.TextInput(attrs={'class': 'form-control'}),
                   'Exp_Month': forms.TextInput(attrs={'class': 'form-control'}),
                   'Exp_Year': forms.TextInput(attrs={'class': 'form-control'}),
                   'CVV': forms.TextInput(attrs={'class': 'form-control'}),


                   }
