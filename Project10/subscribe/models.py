from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone

class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """ Creates and saves a User with the given email, first name, last name,
        and password.
        """
        if not email:
            raise ValueError('Les utilisateurs doivent avoir un email')

        user = self.model(email=self.normalize_email(email),
                          first_name=first_name,
                          last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        """ Creates and saves a superuser with the given email, first name, last name,
        and password.
        """
        user = self.create_user(email=email,
                                first_name=first_name,
                                last_name=last_name,
                                password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address',
                              max_length=255,
                              unique=True)
    first_name = models.CharField(max_length=32, blank=False)
    last_name = models.CharField(max_length=32, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(verbose_name='Date d\'inscription', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='Dernière connexion', auto_now_add=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name',]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
