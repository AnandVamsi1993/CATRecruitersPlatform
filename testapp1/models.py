from asyncio.windows_events import NULL
from unittest.util import _MAX_LENGTH
import uuid
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Group, Permission

from django.db import models

# Create your models here.

class RecruiterManager(BaseUserManager):
    def create_user(self, R_UserName, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        if not R_UserName:
            raise ValueError('The R_UserName field must be set')
        
        recruiter = self.model(R_UserName=R_UserName, **extra_fields)
        recruiter.set_password(password)
        recruiter.save(using=self._db)
        return recruiter

    def create_superuser(self, R_UserName, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(R_UserName, password, **extra_fields)


class Consultant(models.Model):
    C_Id = models.UUIDField(primary_key = True, default= uuid.uuid4, editable = False)
    C_Name = models.CharField(max_length = 100)
    C_Email = models.EmailField(max_length = 200)
    C_Number = models.IntegerField()
    C_Dob = models.DateField(null = True)
    C_Yoe = models.IntegerField()
    C_JobTitles = models.CharField(max_length = 300)

    def __str__(self):
        return self.C_Name


class Recruiter(AbstractBaseUser,PermissionsMixin):
    R_Id = models.UUIDField(primary_key = True, default= uuid.uuid4)
    R_Name = models.CharField(max_length = 100)
    R_UserName = models.CharField(max_length = 50, unique = True)
    #R_Password = models.CharField(max_length = 50 ) ##Can work on password regulatory options

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'R_UserName'
    REQUIRED_FIELDS = ['R_Name']

    objects = RecruiterManager()

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='recruiters'  # Specify a unique related_name for the groups field
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='recruiters'  # Specify a unique related_name for the user_permissions field
    )


    def __str__(self):
        return self.R_Name

    def check_password(self, password_):
        if password_ == self.password:
            return True
        return False

class Submissions(models.Model):
    S_DOS = models.DateField(auto_now_add = True)
    S_RecruiterId = models.ForeignKey(Recruiter, on_delete= models.CASCADE)
    S_ConsultantId = models.ForeignKey(Consultant, on_delete=models.CASCADE)
    S_ConsultantJobTitle = models.CharField(max_length = 100)
    S_ImplementationPartner = models.CharField(max_length = 100)
    S_EndClient = models.CharField(max_length = 100)
    S_EndClientLocation = models.CharField(max_length = 150)
    S_ImplementationPartner_Name = models.CharField(max_length = 100)
    S_ImplementationPartner_Contact = models.IntegerField()

