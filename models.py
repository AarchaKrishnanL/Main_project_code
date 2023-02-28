from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.contrib.auth.models import User

# Create your models here.

# class User(AbstractUser):
#     is_admin= models.BooleanField('Is admin',default=False)
#     is_patient = models.BooleanField('Is patient', default=False)
#     is_doctor = models.BooleanField('Is doctor', default=False)





class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField('User Email')
    phone_number = models.CharField(max_length=10)

    def __str__(self):
        return self.first_name + ' ' + self.last_name + self.email + self.phone_number


class Services(models.Model):
    ser_name = models.CharField(max_length=100,unique=True)
    ser_description = models.TextField()
    ser_image = models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.ser_name

class Doctors(models.Model):
    doc_name = models.CharField(max_length=200,unique=True)
    doc_spec = models.CharField(max_length=200)
    ser_name = models.ForeignKey(Services,on_delete=models.CASCADE)
    doc_image = models.ImageField(upload_to='doctors')

    def __str__(self):
        return self.doc_name


class Time_slot(models.Model):
    time_slot = models.CharField(max_length=100,null=True,blank=True,unique=True)

    def __str__(self):
            return self.time_slot

class Booking(models.Model):
    doc_name= models.ForeignKey(Doctors,on_delete=models.CASCADE)
    booking_date = models.DateField()
    booked_on = models.DateField(auto_now=True)
    time_slot = models.ForeignKey(Time_slot, on_delete=models.CASCADE,null=True,blank=True)
    description = models.TextField(blank=True)


    def __str__(self):
        return self.description

    def clean(self):
        # count the number of existing appointments for the specified time slot and date
        existing_appointments = Booking.objects.filter(
            booking_date=self.booking_date,
            time_slot=self.time_slot
        ).aggregate(num_appointments=Count('id'))['num_appointments']

        # limit the number of appointments to 3 per time slot
        if existing_appointments >= 2:
            raise ValidationError(f"Sorry, the time slot '{self.time_slot}' is already fully booked.")

class Patient(models.Model):
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    mobile = models.IntegerField(null=True)
    address = models.TextField()





class Appointment(models.Model):
    # user = models.ForeignKey(User,on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctors,on_delete=models.CASCADE)
    # ser_name = models.ForeignKey(Services, on_delete=models.CASCADE)
    # patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.ForeignKey(Time_slot, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.doctor} on {self.date} at {self.time}'
    # def __str__(self):
    #     return  self.user + self.doctor + self.patient + self.date + self.time


class Details_User(models.Model):
    blood_group = models.CharField(max_length=3,null=True,blank=True)
    gender = models.CharField(max_length=10,null=True,blank=True)
    age = models.CharField(max_length=3,null=True,blank=True)
    address = models.CharField(max_length=200,null=True,blank=True)
    allergies = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return  self.blood_group + self.gender + self.age + self.address + self.allergies

class Details_Doctor(models.Model):
    doc_name = models.ForeignKey(Doctors, on_delete=models.PROTECT, null=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    age = models.CharField(max_length=3,null=True,blank=True)
    address = models.CharField(max_length=200,null=True,blank=True)
    year_of_experience = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return  self.doc_name + self.gender + self.age + self.address + self.year_of_experience


class Update_Booking(models.Model):
    doc_name= models.ForeignKey(Doctors,on_delete=models.CASCADE)
    booking_date = models.DateField()
    booked_on = models.DateField(auto_now=True)
    time_slot = models.ForeignKey(Time_slot, on_delete=models.CASCADE,null=True,blank=True)
    description = models.TextField(blank=True)


    def __str__(self):
        return self.p_name
