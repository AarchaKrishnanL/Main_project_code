from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from django.core import validators

from . import models
from .models import Booking, Details_User, Details_Doctor,Update_Booking
from django import forms
from django.forms.widgets import DateInput
from django.utils import timezone

# class CustomDateInput(DateInput):
#     input_type = 'date'
#     def __init__(self, *args, **kwargs):
#         super(CustomDateInput, self).__init__(*args, **kwargs)
#         self.attrs['min'] = timezone.now().strftime('%Y-%m-%d')
#
# class MyForm(forms.Form):
#     my_date = forms.DateField(widget=CustomDateInput())



class DateInput(forms.DateInput):
    input_type = 'date'
    def __init__(self, *args, **kwargs):
        super(DateInput, self).__init__(*args, **kwargs)
        self.attrs['min'] = timezone.now().strftime('%Y-%m-%d')

class MyForm(forms.Form):
    my_date = forms.DateField(widget=DateInput())

class TimeInput(forms.TimeField):
    input_type = 'time'

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    phone_number = forms.CharField(max_length=10,min_length=10)
    class Meta:
        model = User
        fields = ('username','first_name','last_name', 'email','password1','password2','phone_number')


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'

        widgets = {
            'booking_date' : DateInput(),
        }

        labels = {
             'doc_name': "Doctor Name: ",
             'booking_date': "Booking Date: ",
             'time_slot': "Slot:",
             'description' : "Description:",
        }

class Details_UserForm(ModelForm):
    class Meta:
        model = Details_User
        fields = '__all__'

        widgets = {
            'blood_group': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Blood Group'}),
            'gender': forms.TextInput(attrs={'class':'form-control','placeholder':'Gender'}),
            'age': forms.TextInput(attrs={'class':'form-control','placeholder':'Age'}),
            'address': forms.TextInput(attrs={'class':'form-control','placeholder':'Address'}),
            'allergies': forms.TextInput(attrs={'class':'form-control','placeholder':'Any Allergies'}),
        }


class Details_DoctorForm(ModelForm):
    class Meta:
        model = Details_Doctor
        fields = '__all__'

        widgets = {
            'doc_name': '',
            'gender': forms.TextInput(attrs={'class':'form-control','placeholder':'Gender'}),
            'age': forms.TextInput(attrs={'class':'form-control','placeholder':'Age'}),
            'address': forms.TextInput(attrs={'class':'form-control','placeholder':'Address'}),
            'year_of_experience': forms.TextInput(attrs={'class':'form-control','placeholder':'Year of Experience'}),
        }


class Update_BookingForm(forms.ModelForm):
    class Meta:
        model = Update_Booking
        fields = '__all__'

        widgets = {
            'booking_date' : DateInput(),
        }

        labels = {
             'doc_name': "Doctor Name: ",
             'booking_date': "Booking Date: ",
             'time_slot': "Slot:",
             'description' : "Description:",
        }

# class DoctorUserForm(forms.ModelForm):
#     class Meta:
#         model=User
#         fields=['first_name','last_name','username','password']
#         widgets = {
#         'password': forms.PasswordInput()
#         }
# class DoctorForm(forms.ModelForm):
#     class Meta:
#         model=models.Doctors
#         fields=['address','mobile','department','status','profile_pic']