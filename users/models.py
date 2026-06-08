from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)
    

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField("Email Address", unique=True)
    phone_number = models.CharField("phone number", max_length=15, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True)
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',
        blank=True
    )

    def __str__(self):
        return self.email
    

class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="addresses", verbose_name="User")
    title = models.CharField("Address Title (eg. Home, Work)", max_length=50)
    receiver_name = models.CharField("Receiver Name", max_length=100)
    receiver_phone = models.CharField("Receiver Phone Number", max_length=15)
    state = models.CharField("State", max_length=100)
    city = models.CharField("City", max_length=100)
    postal_address = models.TextField("Postal Address")
    postal_code = models.CharField("Postal Code", max_length=20)

    def __str__(self):
        return f"{self.title} - {self.user.email}"