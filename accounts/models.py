from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


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


class Profile(AbstractBaseUser):

    userid = models.CharField(max_length=50, unique=True, blank=True, null=False)

    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)

    email = models.EmailField(max_length=254, unique=True, null=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    term_address = models.CharField(max_length=150, blank=True, null=True)

    is_student = models.BooleanField(default=False, null=False)
    is_staff = models.BooleanField(default=False, null=False)
    is_superuser = models.BooleanField(default=False, null=False)

    date_joined = models.DateTimeField(blank=True, null=True)

    objects = ProfileManager()

    USERNAME_FIELD = 'userid'
    REQUIRED_FIELDS = ['email']

    def has_perm(self, perm, obj=None):
        return True

    def has_perms(self, perms, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.userid
