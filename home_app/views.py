from datetime import timezone, timedelta

# import Payment as Payment
from django.contrib.auth import authenticate, login,logout
import subprocess
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, request
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import auth, messages
from django.contrib.auth.models import User, Group
from django.db.models import Q

from tkinter import *
import os


from dental_project import settings
from . import forms, models
from .forms import BookingForm, Details_UserForm, Details_DoctorForm, RegisterUserForm,Update_BookingForm
# from .forms import PatientForm, MedicalHistoryForm, GeneralHealthForm
from .models import Services, Doctors, Booking, Time_slot, Details_User, Update_Booking, Details_Doctor, Appointment, \
    Patients
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PatientForm
# from .forms import DentalForm

# Create your views here.

from django.urls import reverse
import stripe

stripe.api_key = settings.STRIPE_PRIVATE_KEY

# from home_app.forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm


def demo(request):
    return render(request, "doctor_patient.html")

#
# def additional(request):
#     return render(request, "consultation_form.html")

def details_successfull(request):

    return render(request, "details_successfull.html")


def predict(request):
    # print('haiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
    subprocess.run(['python', 'home_app/disease_prediction.py'])
    return redirect("index")




# def predict(request):
#     if request.method == 'POST':
#         # get symptoms from user input
#         symptoms = request.POST.get('symptoms').split(',')
#
#         # load trained Naive Bayes classifier
#         train_df = pd.read_csv('training.csv')
#         test_df = pd.read_csv('testing.csv')
#         X_train = train_df.iloc[:, :-1]
#         y_train = train_df.iloc[:, -1]
#         X_test = test_df.iloc[:, :-1]
#         y_test = test_df.iloc[:, -1]
#         nb_classifier = GaussianNB()
#         nb_classifier.fit(X_train, y_train)
#
#         # prepare symptoms for prediction
#         pred_data = []
#         for i in range(len(X_test.columns)):
#             if X_test.columns[i] in symptoms:
#                 pred_data.append(1)
#             else:
#                 pred_data.append(0)
#
#         # make prediction
#         pred = nb_classifier.predict([pred_data])
#
#         # return predicted disease to user
#         return HttpResponse(f"Based on the symptoms provided, you may have {pred[0]}")
#
#     else:
#         return render(request, 'predict.html')


def payment(request):
    stripe.api_key = settings.STRIPE_PRIVATE_KEY
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1MjGEeSA2phBeRUBBCL7Zaog',
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('thanks')) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri(reverse('front')),
    )

    context = {
        'session_id':session.id,
        'stripe_public_key':settings.STRIPE_PUBLIC_KEY
    }
    return render(request,'payment.html',context)






def thanks(request):
    return render(request, "thanks.html")


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

def bonding(request):
    return render (request,"bonding.html")

def crown(request):
    return render (request,"crown.html")

def veeners(request):
    return render (request,"veeners.html")


def cleaning(request):
    return render (request,"cleaning.html")

def filling(request):
    return render (request,"filling.html")


def time_slot(request):
    dict_timeslot={
        'time_slot':Time_slot.objects.all()
    }
    return render(request, "time_slot.html",dict_timeslot)

# def patient_list(request):
#     patients = Patient.objects.all()
#     return render(request, 'patient_list.html', {'patients': patients})
#
# def patient_form(request):
#     return render(request, "patient_form.html")
# def patient_form(request):
    # if request.method == "POST":
    #     form = PatientForm(request.POST)
    #     if form.is_valid():
    #         blood_group = form.cleaned_data['blood_group']
    #         gender = form.cleaned_data['gender']
    #         dob = form.cleaned_data['dob']
    #         address = form.cleaned_data['address']
    #         allergies = form.cleaned_data['allergies']
    #         records = form.cleaned_data['records']
    #         details_usr=Details_User(blood_group=blood_group,gender=gender,dob=dob,address=address,allergies=allergies,records=records)
    #         details_usr.save()
    #         form = PatientForm
    # # else:
    #     form = PatientForm
    #     patient = Patient.objects.all()
    #     return render(request,'patient_list.html', {'form':form,'patient':patient})

# def patient_create(request):
#     if request.method == 'POST':
#         form = PatientForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('patient_list')
#     else:
#         form = PatientForm()
#     return render(request, 'patient_list.html', {'form': form})
#
# def patient_update(request, pk):
#     patient = get_object_or_404(Patient, pk=pk)
#     if request.method == 'POST':
#         form = PatientForm(request.POST, request.FILES, instance=patient)
#         if form.is_valid():
#             form.save()
#             return redirect('patient_list')
#     else:
#         form = PatientForm(instance=patient)
#     return render(request, 'patient_list.html', {'form': form})
#
# def patient_delete(request, pk):
#     patient = get_object_or_404(Patient, pk=pk)
#     patient.delete()
#     return redirect('patient_list')
#


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

def doc_login(request):
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
            return redirect('doc_login')
    return render(request, "doc_login.html")



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


def my_bookings(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        doc_name = form.cleaned_data['doc_name']
        booking_date = form.cleaned_data['booking_date']
        time_slot = form.cleaned_data['time_slot']
        description = form.cleaned_data['description']
        booking = Booking(doc_name=doc_name, booking_date=booking_date, time_slot=time_slot,
                              description=description)
        booking.save()
        messages.info(request, 'New booking added successfully')
        booking_info = Booking.objects.filter()
        return render(request, 'my_bookings.html', {
                'info': booking_info,
                'doc_name': doc_name,
                'booking_date': booking_date,
                'time_slot': time_slot,
                'description': description,
            })
    if request.user.is_authenticated:
        booking_info = Booking.objects.all()
        # booking_info = Booking.objects.filter()
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

#
# def Update(request,id):
#     if request.method == 'POST':
#         result=Booking.objects.get(id=id)
#         form = BookingForm(request.POST, instance=result)
#         if form.is_valid():
#             form.save()
#     else:
#         result = Booking.objects.get(id=id)
#         form = BookingForm(instance=result)
#         messages.info(request, "Updated!!!")
#     return render(request,'update_booking.html', {'form':form})



def update_details(request, id):
    if request.method == 'POST':
        us = Details_User.objects.get(id=id)
        form = Details_UserForm(request.POST,instance=us)
        if form.is_valid():
            form.save()
    else:
        us = Details_User.objects.get(id=id)
        form = Details_UserForm(request.POST, instance=us)
    return render(request,'update_details.html',{'form':form})

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

def consultation_form(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            gender = form.cleaned_data['gender']
            blood_group = form.cleaned_data['blood_group']
            date_of_birth = form.cleaned_data['date_of_birth']
            previous_report = form.cleaned_data['previous_report']
            supplements = form.cleaned_data['supplements']
            allergies = form.cleaned_data['allergies']
            health_issues = form.cleaned_data['health_issues']
            medications = form.cleaned_data['medications']
            hospitalizations = form.cleaned_data['hospitalizations']
            surgeries = form.cleaned_data['surgeries']
            consultation_form = Patients(gender=gender, blood_group=blood_group, date_of_birth=date_of_birth,
                          previous_report=previous_report,supplements=supplements, allergies=allergies,
                          health_issues=health_issues,medications=medications, hospitalizations=hospitalizations,
                          surgeries=surgeries)
            consultation_form.save()
            # return render(request, 'details_successfull.html')
            messages.info(request, 'Details added successfully')
            consultation_info = Patients.objects.filter()
            return render(request, 'details_successfull.html', {
                'info': consultation_info,
                'gender': gender,
                'blood_group': blood_group,
                'date_of_birth': date_of_birth,
                'previous_report': previous_report,
                'supplements': supplements,
                'allergies': allergies,
                'health_issues': health_issues,
                'medications': medications,
                'hospitalizations': hospitalizations,
                'surgeries': surgeries,
            })

    else:
        form = PatientForm
    return render(request, 'consultation_form.html', {'form': form})









def my_details(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            gender = form.cleaned_data['gender']
            blood_group = form.cleaned_data['blood_group']
            date_of_birth = form.cleaned_data['date_of_birth']
            previous_report = form.cleaned_data['previous_report']
            supplements = form.cleaned_data['supplements']
            allergies = form.cleaned_data['allergies']
            health_issues = form.cleaned_data['health_issues']
            medications = form.cleaned_data['medications']
            hospitalizations = form.cleaned_data['hospitalizations']
            surgeries = form.cleaned_data['surgeries']
            consultation_form = Patients(gender=gender, blood_group=blood_group, date_of_birth=date_of_birth,
                                         previous_report=previous_report, supplements=supplements, allergies=allergies,
                                         health_issues=health_issues, medications=medications,
                                         hospitalizations=hospitalizations,
                                         surgeries=surgeries)
            consultation_form.save()
            messages.info(request, 'Details added successfully')
            consultation_info = Patients.objects.filter()
            return render(request, 'my_details.html', {
                'info': consultation_info,
                'gender': gender,
                'blood_group': blood_group,
                'date_of_birth': date_of_birth,
                'previous_report': previous_report,
                'supplements': supplements,
                'allergies': allergies,
                'health_issues': health_issues,
                'medications': medications,
                'hospitalizations': hospitalizations,
                'surgeries': surgeries,
            })
    if request.user.is_authenticated:
        details_info = Patients.objects.all()
        return render(request, "my_details.html",{
            'info':details_info,
        })
    return redirect('consultation_form')

def services_search(request):
    if request.method == 'GET':
        query = request.GET.get('q')

        if query:
            services = Services.objects.filter(ser_name__icontains=query)
            context = {'services': services, 'query': query}
            return render(request, 'services_search.html', context)

    return redirect('services')

def doctors_search(request):
    query = request.GET.get('q')
    if query:
        doctors = Doctors.objects.filter(
            Q(doc_name__icontains=query)
            # Q(doc_spec__icontains=query) |
            # Q(service__ser_name__icontains=query)
        )
    else:
        doctors = Doctors.objects.all()
    context = {
        'doctors': doctors,
        'query': query
    }
    return render(request, "doctors_search.html", context)








