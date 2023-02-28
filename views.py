from datetime import timezone, timedelta

from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, request
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import auth, messages
from django.contrib.auth.models import User, Group

from dental_project import settings
from . import forms, models
from .forms import BookingForm, Details_UserForm, Details_DoctorForm, RegisterUserForm,Update_BookingForm

from .models import Services, Doctors, Booking, Time_slot, Details_User, Update_Booking, Details_Doctor,Appointment

# Create your views here.

from django.urls import reverse

# from home_app.forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm


def demo(request):
    return render(request, "doctor_patient.html")

def front(request):
    return render(request, "front.html")

def about(request):
    return render(request, "about.html")

def doctor_page(request):
    return render(request, "doctor_page.html")

def update_booking(request):
    return render(request, "update_booking.html")

def loginn(request):
    return render(request, "registration/loginn.html")

def doctor_patient(request):
    return render(request, "doctor_patient.html")


def doctor_register(request):
    return render(request, "doctor_register.html")

def time_slot(request):
    dict_timeslot={
        'time_slot':Time_slot.objects.all()
    }
    return render(request, "time_slot.html",dict_timeslot)



def booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            doc_name=form.cleaned_data['doc_name']
            booking_date = form.cleaned_data['booking_date']
            time_slot = form.cleaned_data['time_slot']
            description = form.cleaned_data['description']
            booking = Booking(doc_name=doc_name,booking_date=booking_date,time_slot=time_slot,description=description)
            booking.save()
            messages.info(request,'New booking added successfully')
            booking_info=Booking.objects.filter()
            return render(request, 'my_bookings.html',{
                'info':booking_info,
                'doc_name':doc_name,
                'booking_date':booking_date,
                'time_slot':time_slot,
                'description':description,
            })
    else:
        form=BookingForm
    return render(request,'booking.html',{'form':form})




# def booking(request):
#     if request.user.is_authenticated:
#         if request.method == "POST":
#             form = BookingForm(request.POST)
#             if form.is_valid():
#                 doc_name=form.cleaned_data['doc_name']
#                 booking_date = form.cleaned_data['booking_date']
#                 time_slot = form.cleaned_data['time_slot']
#                 description = form.cleaned_data['description']
#             if booking_date < timezone.now().booking_date():
#                 messages.info(request, "Date cannot be in the past")
#                 return redirect('booking')
#             startdate = booking_date
#             enddate = startdate + timedelta(days=0)
#             doctors_service = Booking.objects.filter(date__range=[startdate, enddate]).values_list('doc_name').filter(
#                 doc_name=doc_name).count()
#             todays_slot = Booking.objects.filter(date__range=[startdate, enddate]).values_list('time').filter(
#                 doc_name=doc_name).filter(time=time_slot).count()
#             count_per_day = Booking.objects.filter(date__range=[startdate, enddate]).count()
#             # if count_per_day > 5:
#             #     messages.info(request, "Appointment is full for this date!! Try another date!")
#             #     return redirect('booking')
#             if doctors_service > 4:
#                 messages.info(request, "Appointment is full for this service!! Try another day!")
#                 return redirect('appointment')
#             elif todays_slot > 2:
#                 messages.info(request, "Appointment is full for this time slot!! Try another time slot!")
#                 return redirect('appointment')
#                 # print(result)
#                 # print(count_per_day)
#                 print(todays_aptmnt)
#                 print(todays_slot)
#             booking = Booking(doc_name=doc_name,booking_date=booking_date,time_slot=time_slot,description=description)
#             booking.save()
#             messages.info(request,'New booking added successfully')
#             booking_info=Booking.objects.filter(user=request.user)
#             return render(request, 'my_bookings.html',{
#                 'info':booking_info,
#                 'doc_name':doc_name,
#                 'booking_date':booking_date,
#                 'time_slot':time_slot,
#                 'description':description,
#             })
#         else:
#              form=BookingForm
#         return render(request,'booking.html',{'form':form})
#     return redirect('login')





def doctors(request):
    dict_docs = {
        'doctors': Doctors.objects.all()
    }
    return render(request, "doctors.html", dict_docs)


def contact(request):
    return render(request, "contact.html")


def services(request):
    dict_services={
        'services':Services.objects.all()
    }
    return render(request, "services.html",dict_services)


def user_login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request,"Invalid credentials")
            return redirect('login')
    return render(request, "login.html")


#def register(request):
   # form = CustomUserCreationForm()
  #  if request.method =='POST':
    #    form = CustomUserCreationForm(request.POST)
    #    if form.is_valid():
     #       form.save()
     #       return render(request, 'register_confirmation.html')
   # return render(request,'register.html',{'form':form})

def register(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            login(request,user)
            return render(request, 'register_confirmation.html')
            return redirect('/')
    else:
        form = RegisterUserForm()

    return render(request,'register.html',{'form':form,})







def index(request):
    return render (request,"index.html")

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('/')

def user(request):
    if request.user.is_authenticated:
        return render(request, "index.html")
    return redirect('login')

# def my_bookings(request):
#     if request.user.is_authenticated:
#         booking_info = {
#          'booking': Booking.objects.all()
#      }
#     return render(request, "my_bookings.html", booking_info)

def my_bookings(request):
    if request.user.is_authenticated:
        # booking_info = Booking.objects.all()
        booking_info = Booking.objects.filter(user_id=request.user.id)
        return render(request, "my_bookings.html",{
            'info':booking_info,
        })
    return redirect('booking')

# CRUD OPERATIONS
def Delete(request,id):
    booking_info = Booking.objects.filter(id=id)
    booking_info.delete()
    messages.info(request, "Appointment Deleted!!!")
    return redirect("my_bookings")


def Update(request,id):
    if request.method == 'POST':
        result=Booking.objects.get(id=id)
        form = BookingForm(request.POST, instance=result)
        if form.is_valid():
            form.save()
    else:
        result = Booking.objects.get(id=id)
        form = BookingForm(instance=result)
        messages.info(request, "Updated!!!")
    return render(request,'update_booking.html', {'form':form})

def details_user(request):
    submitted = False
    if request.method == "POST":
        form = Details_UserForm(request.POST)
        if form.is_valid():
            blood_group = form.cleaned_data['blood_group']
            gender = form.cleaned_data['gender']
            age = form.cleaned_data['age']
            address = form.cleaned_data['address']
            allergies = form.cleaned_data['allergies']
            details_usr=Details_User(blood_group=blood_group,gender=gender,age=age,address=address,allergies=allergies)
            details_usr.save()
            form = Details_UserForm
    else:
        form = Details_UserForm
    userdetails = Details_User.objects.all()
    return render(request,'details_user.html', {'form':form,'userdetails':userdetails})

def update_user(request, id):
    if request.method == 'POST':
        us = Details_User.objects.get(id=id)
        form = Details_UserForm(request.POST,instance=us)
        if form.is_valid():
            form.save()
    else:
        us = Details_User.objects.get(id=id)
        form = Details_UserForm(request.POST, instance=us)
    return render(request,'update_user.html',{'form':form})

# def view_user(request):
#     if request.user.is_authenticated:
#         user_info = Details_User.objects.filter(user=request.user)
#         return render(request, "update_user.html",{
#             'info':user_info,
#         })


# def update_userdetails(request):
#     if request.user.is_authenticated:
#         user_info = Details_User.objects.filter(user=request.user)
#         return render(request, "update_user.html",{
#             'info':user_info,
#         })


# def details_doctor(request):
#     submitted = False
#     if request.method == "POST":
#         form = Details_DoctorForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/details_doctor?submitted=True')
#     else:
#         form = Details_DoctorForm
#         if 'submitted' in request.GET:
#             submitted = True
#     return render(request,'details_doctor.html', {'form':form, 'submitted':submitted})

def details_doctor(request):
    submitted = False
    if request.method == "POST":
        form = Details_DoctorForm(request.POST)
        if form.is_valid():
            gender = form.cleaned_data['gender']
            age = form.cleaned_data['age']
            address = form.cleaned_data['address']
            year_of_experience = form.cleaned_data['year_of_experience']
            details_dtr=Details_Doctor(gender=gender,age=age,address=address,year_of_experience=year_of_experience)
            details_dtr.save()
            form = Details_DoctorForm
    else:
        form = Details_DoctorForm
    doctordetails = Details_Doctor.objects.all()
    return render(request,'details_user.html', {'form':form,'doctordetails':doctordetails})

def update_doctor(request, id):
    if request.method == 'POST':
        dr = Details_Doctor.objects.get(id=id)
        form = Details_UserForm(request.POST,instance=dr)
        if form.is_valid():
            form.save()
    else:
        us = Details_Doctor.objects.get(id=id)
        form = Details_DoctorForm(request.POST, instance=us)
    return render(request,'update_doctor.html',{'form':form})

def update_booking(request):
    if request.method == "POST":
        form = Update_BookingForm(request.POST)
        if form.is_valid():
            doc_name=form.cleaned_data['doc_name']
            booking_date = form.cleaned_data['booking_date']
            time_slot = form.cleaned_data['time_slot']
            description = form.cleaned_data['description']
            booking = Update_Booking(doc_name=doc_name,booking_date=booking_date,time_slot=time_slot,description=description)
            booking.save()
            messages.info(request,'New booking added successfully')
            booking_info=Update_Booking.objects.filter()
            return render(request, 'my_bookings.html',{
                'info':booking_info,
                'doc_name':doc_name,
                'booking_date':booking_date,
                'time_slot':time_slot,
                'description':description,
            })
    else:
        form=BookingForm
    return render(request,'booking.html',{'form':form})




# def doctor_signup_view(request):
#     userForm=forms.DoctorUserForm()
#     doctorForm=forms.DoctorForm()
#     mydict={'userForm':userForm,'doctorForm':doctorForm}
#     if request.method=='POST':
#         userForm=forms.DoctorUserForm(request.POST)
#         doctorForm=forms.DoctorForm(request.POST,request.FILES)
#         if userForm.is_valid() and doctorForm.is_valid():
#             user=userForm.save()
#             user.set_password(user.password)
#             user.save()
#             doctor=doctorForm.save(commit=False)
#             doctor.user=user
#             doctor=doctor.save()
#             my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
#             my_doctor_group[0].user_set.add(user)
#         return HttpResponseRedirect('login')
#     return render(request,'register.html',context=mydict)


# def doctor_view_bookings(request):
#     if request.user.is_authenticated:
#         bookings_info = Booking.objects.all()
#
#         # booking_info = Booking.objects.filter(user=request.user)
#         return render(request, "doctor_view_bookings.html",{
#             'info':bookings_info,
#         })







