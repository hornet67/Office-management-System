from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.core.validators import MinValueValidator, MaxValueValidator 
from django.contrib.auth.hashers import make_password

# Create your models here.

#modification of users/owners of the application
class User(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True , validators=[MinValueValidator(18), MaxValueValidator(70)])
    phone_number = models.CharField(max_length=11, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.username
    
    
    
    
    
        

class Company_type(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    
class Company_info(models.Model):
    company_id = models.AutoField(primary_key=True,unique=True)
    company_name = models.CharField(max_length=300)
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=11, blank=True)
    type = models.ForeignKey(Company_type, on_delete=models.CASCADE)
    address = models.TextField()
    website = models.URLField(max_length=200, blank=True)
    domain = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.company_name 
    

class User_role(models.Model):
    role = models.CharField(max_length=100)

    def __str__(self):
        return self.role



class User_info(models.Model):
    gender = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    
    religion = [
        ('Islam', 'Islam'),
        ('Hindu', 'Hindu'),
        ('Buddhism', 'Buddhism'),
        ('Christianity', 'Christianity'),
        ('Other', 'Other'),
    ]
    
    user_id = models.AutoField(primary_key=True,unique=True)
    title = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=11)
    gender = models.CharField(max_length=10, choices=gender)
    address = models.TextField( blank=True)
    role = models.ForeignKey(User_role, on_delete=models.CASCADE) #relationship with user role table
    dob = models.DateField(blank=True)
    religion = models.CharField(max_length=15, choices=religion)
    nid = models.CharField(max_length=100, null=False, blank=False)
    passport = models.CharField(max_length=100, null=False, blank=False)
    driving_license = models.CharField(max_length=100, null=False, blank=False)
    corporate_id = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=128, null=False, blank=False)
    image = models.ImageField(upload_to='user_images/', null=True, blank=True)
    company = models.ForeignKey(Company_info, on_delete=models.CASCADE) #relationship with company table and use table
    
    is_active = models.BooleanField(default=False)
    activated_by = models.ForeignKey('Auth_system.User',on_delete=models.SET_NULL, null=True, blank=True, related_name='activated_users')
    activated_at = models.DateTimeField(null=True, blank=True)
    
    
    @property
    def activated_by_name(self):
        return self.activated_by.name if self.activated_by else "Not activated"
    
    
    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith("pbkdf2_"):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.company.company_name + " - " + self.name