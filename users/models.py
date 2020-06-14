from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from contacts.models import Contact


class UserManager(BaseUserManager):
    def _create_user(self, mobile, password, **kwargs):
        if not mobile:
            raise ValueError('Mobile is required.')
        user = self.model(mobile=mobile, **kwargs)
        user.set_password(password)
        user.save()
        return user
    
    def create_user(self, mobile, password, **kwargs):
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        kwargs.setdefault('is_active', True)
        return self._create_user(mobile, password, **kwargs)
    
    def create_superuser(self, mobile, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must be a staff')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must be a superuser')
        return self._create_user(mobile, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into the django admin panel.'),
    )
    is_active = models.BooleanField(_('active'), default=True)

    mobile = PhoneNumberField(unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    full_name = models.CharField(max_length=255)

    date_joined = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now_add=True)

    contacts = models.ManyToManyField(Contact, blank=True)

    USERNAME_FIELD = 'mobile'

    objects = UserManager()

    def __str__(self):
        return "{} - {}".format(str(self.mobile), self.full_name)
    
    def save(self, *args, **kwargs):
        if not self.id:
            contact = Contact(
                owner=self,
                full_name=self.full_name,
                mobile=self.mobile
            )
            super().save(*args, **kwargs)
            contact.save()
        super().save(*args, **kwargs)
        
