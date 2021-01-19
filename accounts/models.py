from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _


class ProfileManager(BaseUserManager):
    """Manager class for the Profile model"""

    def create_user(self, userid, email, password=None):
        user = self.model(
            userid=userid,
            password=password,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_or_create_user(self, userid, email, password=None):
        user = Profile.objects.filter(userid=userid)
        if user.exists():
            return user[0], False
        else:
            return self.create_user(userid, email, password), True

    def create_superuser(self, userid, email, password=None):
        user = self.create_user(
            userid,
            password=password,
            email=email,
        )
        user.is_superuser = True
        staff_group, created = Group.objects.get_or_create(name='staff')
        staff_group.user_set.add(user)
        user.save(using=self._db)
        return user

    def get_or_create_superuser(self, userid, email, password=None):
        user = Profile.objects.filter(userid=userid)
        if user.exists():
            return user[0], False
        else:
            return self.create_superuser(userid, email, password), True


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

    date_joined = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    objects = ProfileManager()

    USERNAME_FIELD = 'userid'
    REQUIRED_FIELDS = ['email']

    @property
    def is_staff(self):
        return self.groups.filter(name='staff').exists() or self.is_superuser

    @property
    def is_student(self):
        return self.groups.filter(name='student').exists()

    def __str__(self):
        return self.userid

    class Meta:
        ordering = ['first_name', 'last_name', 'userid']
        indexes = [
            models.Index(fields=['first_name', 'last_name']),
            models.Index(fields=['email']),
            models.Index(fields=['date_joined']),
        ]


class AccountSubmission(models.Model):
    email = models.EmailField(max_length=254, null=False)
    course = models.ForeignKey('courses.Course', on_delete=models.SET_NULL, null=True)

    valid = models.BooleanField(default=True)

    date_submitted = models.DateTimeField(null=True, auto_now_add=True)

    class Meta:
        unique_together = ('email', 'course')
        ordering = ['date_submitted']
        indexes = [
            models.Index(fields=['date_submitted']),
            models.Index(fields=['course']),
        ]
        permissions = [
            ('can_accept', 'Can accept course submissions'),
            ('can_reject', 'Can reject course submissions'),
            ('can_add', 'Can add course submission to any new account')
        ]
        default_permissions = []
