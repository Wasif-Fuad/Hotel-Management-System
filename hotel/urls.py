from unicodedata import name
from django.urls import path

from hotel.models import RoomCategory
from .import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from employeeRec import urls


urlpatterns = [
    path('', views.home, name='home'),
    path('<int:id>', views.show, name='show'),
    path('register/', views.registerPage, name="register"),
    path('register/emp', views.registerPageEmp, name="registeremp"),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('login/Register.html', views.registerPage, name='register'),

    path('register/Login.html', views.registerPage, name='register'),
    path('hotels/Register.html', views.registerPage, name='register'),
    # path('deshboard/', views.deshBoard, name='deshboard'),
    path('contact/', views.contactus, name='contact'),
    path('hotelsection/', views.hotelsection, name="hotelsection"),
    path('booking/<room_category>', views.bookingForm, name="booking"),
    path('employeeRec/index/', views.employee, name='employee'),
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="hotel/password_reset.html"), name="reset_password"),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="hotel/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="hotel/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="hotel/password_reset_done.html"),
         name="password_reset_complete"),

    path('rooms', views.rooms, name='rooms'),
    path('profile', views.profile, name='profile'),
    path('booking/confirmation/<int:booking_id>',
         views.booking_confirm, name='confirm-booking'),

    path('task', views.task_admin, name='task'),
    path('mytask', views.mytask, name='mytask'),
    path('addroom', views.addroom, name='addroom'),
    path('addcategory', views.addcategory, name='addcategory'),
    path('booking/confirmation/payment/<int:booking_id>',
         views.paymentt, name='payment'),
    path('history', views.history, name='history'),
    path('approval', views.approval, name='approval'),
    path('delete_booking/<int:bid>', views.delete_booking, name='delete-booking'),
    path('delete_task/<int:bid>', views.delete_task, name='delete-task'),
    path('delete_employee/<str:name>',
         views.delete_employee, name='delete-employee'),
    path('delete_category/<int:bid>',
         views.delete_category, name='delete-category'),
    path('update_category/<int:bid>',
         views.update_category, name='update-category'),
          path('delete_room/<int:bid>',
         views.delete_room, name='delete-room'),

]
