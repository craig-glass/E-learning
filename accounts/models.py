from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _


class ProfileManager(BaseUserManager):
    def create_user(self, userid, email, password=None):
        user = self.model(
            userid=userid,
            password=password,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, userid, email, password=None):
        user = self.create_user(
            userid,
            password=password,
            email=email,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Profile(AbstractBaseUser, PermissionsMixin):
    userid = models.CharField(
        max_length=50, unique=True, blank=True, null=False,
        help_text=_('Unique identifier for the account')
    )

    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)

    email = models.EmailField(max_length=254, unique=True, null=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    term_address = models.CharField(max_length=150, blank=True, null=True)

    is_student = models.BooleanField(
        default=False, null=False,
        help_text=_('Designate status as a student')
    )
    is_staff = models.BooleanField(
        default=False, null=False,
        help_text=_('Designate status as a member of staff')
    )

    date_joined = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    objects = ProfileManager()

    USERNAME_FIELD = 'userid'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.userid


def set_default_groups(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        if user.is_student:
            student_group, created = Group.objects.get_or_create(name='student')
            user.groups.add(student_group)
        if user.is_staff:
            staff_group, created = Group.objects.get_or_create(name='staff')
            user.groups.add(staff_group)
        if user.is_superuser:
            superuser_group, created = Group.objects.get_or_create(name='superuser')
            user.groups.add(superuser_group)
