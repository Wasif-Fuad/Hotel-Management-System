from django.contrib import admin
from .models import Room

from .models import BookingRoom
from .models import UserProfiles
from .models import ContactUs
from .models import RoomCategory, RoomNumber, StaffTask, payment, Staff

# Register your models here.

admin.site.register(Room)

admin.site.register(RoomCategory)
admin.site.register(BookingRoom)
admin.site.register(UserProfiles)
admin.site.register(ContactUs)
admin.site.register(RoomNumber)
admin.site.register(StaffTask)
admin.site.register(payment)
admin.site.register(Staff)
