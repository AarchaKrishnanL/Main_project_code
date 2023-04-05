from datetime import datetime

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
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

from .models import Patients
# class CustomDateInput(DateInput):
#     input_type = 'date'
#     def __init__(self, *args, **kwargs):
#         super(CustomDateInput, self).__init__(*args, **kwargs)
#         self.attrs['min'] = timezone.now().strftime('%Y-%m-%d')
#
# class MyForm(forms.Form):
#     my_date = forms.DateField(widget=CustomDateInput())

class CustomDateInput(forms.DateInput):
    input_type = 'date'
    def __init__(self, *args, **kwargs):
        super(CustomDateInput, self).__init__(*args, **kwargs)
        today = timezone.now().strftime('%Y-%m-%d')
        # self.attrs['min'] = today
        self.attrs['max'] = today

class MForm(forms.Form):
    my_date = forms.DateField(widget=CustomDateInput())

# class PatientForm(forms.ModelForm):
#     class Meta:
#         model = Patient
#         fields = '__all__'
#
#         widgets = {
#             'dob': CustomDateInput()
#         }
#         # widgets = {
#         #     'dob': forms.DateInput(attrs={'type': 'date'}),
#         # }
#
#     def clean_records(self):
#         records = self.cleaned_data['records']
#         if records and not records.name.endswith('.pdf'):
#             raise forms.ValidationError('Only PDF files are allowed.')
#         return records



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


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patients
        fields = '__all__'  # You can also specify individual fields here

        widgets = {
            'date_of_birth': CustomDateInput(),
        }

# class MedicalHistoryForm(forms.ModelForm):
#     class Meta:
#         model = MedicalHistory
#         exclude = ['patient']  # Exclude the patient field from the form
#
# class GeneralHealthForm(forms.ModelForm):
#     class Meta:
#         model = GeneralHealth
#         exclude = ['patient']  # Exclude the patient field from the form



