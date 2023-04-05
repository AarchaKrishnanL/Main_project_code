from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
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
    doc_name= models.ForeignKey(Doctors,on_delete=models.CASCADE,null=True,blank=True)
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

        # limit the number of appointments to 2 per time slot
        if existing_appointments >= 2:
            raise ValidationError(f"Sorry, the time slot '{self.time_slot}' is already fully booked.")

class Patients(models.Model):
    GENDER_CHOICES = [
        ('female', 'Female'),
        ('male', 'Male'),
        ('other', 'Other'),
    ]

    BLOOD_GROUP_CHOICES = [
        ('O+', 'O+'),
        ('A+', 'A+'),
        ('B+', 'B+'),
        ('AB+', 'AB+'),
        ('O-', 'O-'),
        ('A-', 'A-'),
        ('B-', 'B-'),
        ('AB-', 'AB-'),
    ]

    gender = models.CharField(max_length=6, choices=GENDER_CHOICES,null=True,blank=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES,null=True,blank=True)
    date_of_birth = models.DateField(null=True,blank=True)
    previous_report = models.FileField(upload_to='previous_reports/',null=True,blank=True)
    supplements = models.TextField(blank=True,null=True)
    allergies = models.TextField(blank=True,null=True)
    health_issues = models.TextField(blank=True,null=True)
    medications = models.TextField(blank=True,null=True)
    hospitalizations = models.TextField(blank=True,null=True)
    surgeries = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.gender + self.blood_group + self.date_of_birth






class Appointment(models.Model):
    # user = models.ForeignKey(User,on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctors,on_delete=models.CASCADE)
    # ser_name = models.ForeignKey(allservices, on_delete=models.CASCADE)
    # patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.ForeignKey(Time_slot, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.doctor} on {self.date} at {self.time}'
    # def __str__(self):
    #     return  self.user + self.doctor + self.patient + self.date + self.time


class Details_User(models.Model):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    ]

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    ALLERGY_CHIOCES = [
        ('Yes','Yes'),
        ('No','No')
    ]

    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES,null=True,blank=True,unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,null=True, blank=True)
    age = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(120)],null=True, blank=True)
    address = models.CharField(max_length=200, validators=[RegexValidator('^[\w\s]+$', message="Address must only contain letters, digits, and spaces.")],null=True, blank=True)
    allergies = models.CharField(max_length=3,choices=ALLERGY_CHIOCES,null=True, blank=True)

    def __str__(self):
        return  self.blood_group + self.gender + self.age + self.address + self.allergies


class Details_Doctor(models.Model):

    gender = models.CharField(max_length=10, null=True, blank=True)
    age = models.CharField(max_length=3,null=True,blank=True)
    address = models.CharField(max_length=200,null=True,blank=True)
    year_of_experience = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return   self.gender + self.age + self.address + self.year_of_experience


class Update_Booking(models.Model):
    doc_name= models.ForeignKey(Doctors,on_delete=models.CASCADE)
    booking_date = models.DateField()
    booked_on = models.DateField(auto_now=True)
    time_slot = models.ForeignKey(Time_slot, on_delete=models.CASCADE,null=True,blank=True)
    description = models.TextField(blank=True)


    def __str__(self):
        return self.p_name


