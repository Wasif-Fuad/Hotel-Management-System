
from asyncio.windows_events import NULL
from .forms import CreateUserForm, UserProfileForm, StaffTaskForm, CreateCategoryform, PaymentForm
from audioop import reverse
from itertools import chain
from multiprocessing import context
from pyexpat import model
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
# from django.views.decorators.cache import cache_page
# from django.core.cache import cache
from django.views.generic import ListView, FormView

from hotel.decorators import unauthenticated_user
from .models import Room, UserProfiles, StaffTask, RoomNumber, payment

from .forms import ContactForm, BookingRoomForm, UserProfileForm, CreateRoomform

from hotel.bookingFunctions.availability import check_availability

from .decorators import unauthenticated_user, allowed_users, admin_only
# Create your views here.
from .models import *

# CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def registerPage(request):
    puser = 0
    if(request.user.is_authenticated and not request.user.is_superuser):
        puser = UserProfiles.objects.get(user=request.user)
    if request.user.is_authenticated:
        return redirect('home')

    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            form2 = UserProfiles()

            if form.is_valid():
                form.save()

                form2.user = form.cleaned_data.get('username')
                form2.FirstName = form.cleaned_data.get('first_name')
                form2.LastName = form.cleaned_data.get('last_name')
                form2.Email = form.cleaned_data.get('email')
                form2.DateofBirth = request.POST['dofb']
                form2.need_approve = False
               # form2.user = User.objects.get(username=user3)
               # form2.user = user3
                form2.save()

                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')

                return redirect('login')

    context = {'form': form, 'puser': puser}
    return render(request, 'hotel/Register.html', context)


def registerPageEmp(request):
    puser = 0
    if(request.user.is_authenticated and not request.user.is_superuser):
        puser = UserProfiles.objects.get(user=request.user)
    if request.user.is_authenticated:
        return redirect('home')

    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            form2 = UserProfiles()

            if form.is_valid():
                form.save()

                form2.user = form.cleaned_data.get('username')
                form2.FirstName = form.cleaned_data.get('first_name')
                form2.LastName = form.cleaned_data.get('last_name')
                form2.Email = form.cleaned_data.get('email')
                form2.DateofBirth = request.POST['dofb']
               # form2.user = User.objects.get(username=user3)
               # form2.user = user3
                form2.save()

                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')

                return redirect('login')

    context = {'form': form, 'puser': puser}
    return render(request, 'hotel/Register.html', context)


def loginPage(request):
    puser = 0
    if(request.user.is_authenticated and not request.user.is_superuser):
        puser = UserProfiles.objects.get(user=request.user)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR Password is incorrect')

    context = {'puser': puser}
    return render(request, 'hotel/Login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


""""
@login_required(login_url='login')
def deshBoard(request):
    context = {}
    return render(request, 'hotel/deshboard.html', context)
"""


def get_room(filter_room=None):
    if filter_room:
        print("DATA COMING FROM DB")
        room = Room.objects.filter(category__contains=filter_room)
    else:
        room = Room.objects.all()
    return room


def home(request):
    filter_room = request.GET.get('room')
    puser = 0
    if(request.user.is_authenticated and not request.user.is_superuser):
        puser = UserProfiles.objects.get(user=request.user)

    if(request.user.is_authenticated):
        if request.user.is_superuser:
            return redirect('rooms')
        if puser.is_staff:
            return redirect('mytask')

    if filter_room:
        room = get_room(filter_room)
          
    else:
        room = get_room()
    context = {'room': room, 'puser': puser}
    return render(request, 'hotel/home.html', context)

# @login_required(login_url='login')


def show(request, id):
    puser = 0
    if(request.user.is_authenticated and not request.user.is_superuser):
        puser = UserProfiles.objects.get(user=request.user)
 
    room = Room.objects.get(id=id)
       
    context = {'room': room, 'puser': puser}
    return render(request, 'hotel/show.html', context)


@login_required(login_url='login')
def employee(request):
    return render(request, 'employeeRec/index.html')


def hotelsection(request):
    return render(request, 'hotel/home.html')


def contactus(request):
    puser = 0
    if(request.user.is_authenticated and not request.user.is_superuser):
        puser = UserProfiles.objects.get(user=request.user)
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            return render(request, 'hotel/home.html')
    else:
        form = ContactForm()
    return render(request, 'hotel/contact.html', {'form': form, 'puser': puser})


@login_required(login_url='login')
def bookingForm(request, room_category):
    puser = 0
    if(request.user.is_authenticated and not request.user.is_superuser):
        puser = UserProfiles.objects.get(user=request.user)
    r = Room.objects.get(category=room_category)
    booking = BookingRoom()
    booking.user = request.user
    room = RoomNumber.objects.filter(category=r)

    if room:
        booking.room = room[0]
    else:
        messages.success(request, 'No rooms available')
        return redirect('home')

    if (request.method == 'POST'):
        #form = BookingRoomForm(request.POST)
        booking.check_in = request.POST['check-in']
        booking.check_out = request.POST['check-out']

        booking.save()
        return redirect("confirmation/"+f'{booking.id}')

    return render(request, 'hotel/booking_form.html', {'puser': puser})


def rooms(request):
    puser = 0
    if(request.user.is_authenticated and not request.user.is_superuser):
        puser = UserProfiles.objects.get(user=request.user)
    filter_room = request.GET.get('room')
  
    if filter_room:
        room = get_room(filter_room)
         
    else:
            room = get_room()
    context = {'room': room, 'puser': puser}
    return render(request, 'hotel/rooms.html', context)


def profile(request):
    puser = 0
    history = None
    if(request.user.is_authenticated and not request.user.is_superuser):
        puser = UserProfiles.objects.get(user=request.user)
    tuser = User.objects.get(pk=request.user.id)
    user1 = UserProfiles.objects.get(user=tuser.username)

    if not user1.is_staff:
        his = payment.objects.filter(user=request.user)
        if his:
            history = PaymentForm(request.POST or None, instance=his[0])
            if history.is_valid():
                history.save()
                return redirect('profile')
        form = UserProfileForm(request.POST or None, instance=user1)
    else:
        form = UserProfileForm(request.POST or None, instance=user1)

    if form.is_valid():
        form.save()
        return redirect('profile')

    return render(request, 'hotel/profile.html', {'form': form, 'history': history, 'puser': puser})


def booking_confirm(request, booking_id):
    puser = 0
    if(request.user.is_authenticated and not request.user.is_superuser):
        puser = UserProfiles.objects.get(user=request.user)
    booking = BookingRoom.objects.get(pk=booking_id)
    booking.total_bill = booking.bill()
    booking.save()
    if request.method == 'POST':
        return redirect('payment/'+f'{booking.id}')
    else:
        if booking:
            return render(request, 'hotel/booking_confirm.html', {'booking': booking, 'puser': puser})
        else:
            return HttpResponse("404 Page not found")


def task_admin(request):
    puser = 0
    if(request.user.is_authenticated and not request.user.is_superuser):
        puser = UserProfiles.objects.get(user=request.user)
    if (request.method == "POST"):

        form = StaffTaskForm(request.POST)

        if form.is_valid():
            form.save()
            #work.assigned = request.POST['assigned']
            # work.deadline = request.POST['deadline']
            # work.save()

            return redirect('task')

    else:
        form = StaffTaskForm()
        tasks = StaffTask.objects.filter(complete=False)

    return render(request, 'hotel/task_admin.html', {'form': form, 'tasks': tasks, 'puser': puser})


def mytask(request):
    puser = 0
    if(request.user.is_authenticated and not request.user.is_superuser):
        puser = UserProfiles.objects.get(user=request.user)
    st = Staff.objects.get(name=puser)
    tasks = StaffTask.objects.filter(user=st)
    return render(request, 'hotel/mytask.html', {'tasks': tasks, 'puser': puser})


def addroom(request):
    puser = 0
    if(request.user.is_authenticated and not request.user.is_superuser):
        puser = UserProfiles.objects.get(user=request.user)
    room = RoomNumber.objects.all()
    if(request.method == "POST"):
        form = CreateRoomform(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('addroom')
    else:
        form = CreateRoomform()

    return render(request, 'hotel/addroom.html', {'form': form, 'room': room, 'puser': puser})


def paymentt(request, booking_id):
    puser = 0
    if(request.user.is_authenticated and not request.user.is_superuser):
        puser = UserProfiles.objects.get(user=request.user)
    booking = BookingRoom.objects.get(pk=booking_id)

    his = payment.objects.filter(user=request.user)

    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False)

            p.user = request.user
            booking.status = True
            booking.save()
            p.save()
            return redirect('history')
        else:
            return render(request, 'hotel/payment.html', {'form': form, 'puser': puser})
    elif his:
        form = PaymentForm(instance=his[0])
    else:
        form = PaymentForm()

    return render(request, 'hotel/payment.html', {'form': form, 'puser': puser})


def history(request):
    puser = 0
    if(request.user.is_authenticated and not request.user.is_superuser):
        puser = UserProfiles.objects.get(user=request.user)

    history = BookingRoom.objects.filter(user=request.user, status=True)

    return render(request, 'hotel/booking_list.html', {'history': history, 'puser': puser})


def addcategory(request):
    puser = 0
    if(request.user.is_authenticated and not request.user.is_superuser):
        puser = UserProfiles.objects.get(user=request.user)
    if(request.method == "POST"):
        form = CreateCategoryform(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('rooms')
    else:
        form = CreateCategoryform()

    return render(request, 'hotel/addcategory.html', {'form': form, 'puser': puser})


@login_required(login_url='login')
def approval(request):
    tuser = User.objects.get(pk=request.user.id)
    user1 = UserProfiles.objects.filter(need_approve=True)

    puser = None

    staff = UserProfiles.objects.filter(is_staff=True)
    if(request.user.is_authenticated and not request.user.is_superuser):
        puser = UserProfiles.objects.get(user=request.user)

    if request.method == "POST":
        id_list = request.POST.getlist('boxes')

        for x in id_list:
            ob = UserProfiles.objects.get(pk=int(x))
            st = Staff()
            st.name = ob
            st.save()
            ob.is_staff = True
            ob.need_approve = False
            ob.save()
        return redirect('approval')
    else:
        return render(request, 'hotel/approval.html', {'user1': user1, 'puser': NULL, 'staff': staff})


def delete_booking(request, bid):
    ob = BookingRoom.objects.get(pk=bid)
    ob.delete()
    return redirect('history')


def delete_task(request, bid):
    ob = StaffTask.objects.get(pk=bid)
    ob.delete()
    return redirect('mytask')


def delete_employee(request, name):
    ob = UserProfiles.objects.get(user=name)
    ob1 = User.objects.get(username=name)
    ob1.delete()
    ob.delete()
    return redirect('approval')


def delete_category(request, bid):
    ob = Room.objects.get(pk=bid)
    ob.delete()
    return redirect('rooms')


def update_category(request, bid):
    puser = 0
    if(request.user.is_authenticated and not request.user.is_superuser):
        puser = UserProfiles.objects.get(user=request.user)

    room = Room.objects.get(pk=bid)
    form = CreateCategoryform(request.POST or None, instance=room)

    if form.is_valid():
        form.save()
        return redirect('rooms')
    return render(request, 'hotel/updatecategory.html', {'form': form,  'puser': puser})


def delete_room(request, bid):
    ob = RoomNumber.objects.get(pk=bid)
    ob.delete()
    return redirect('addroom')
