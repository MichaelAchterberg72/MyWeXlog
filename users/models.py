from django.db import models
from django.conf import settings
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, UserManager

class CustomUserManager(UserManager):
    pass

class CustomUser(AbstractUser):
    PKG = (
        (0,'Free'),
        (1,'Passive'),
        (2,'Active'),
    )
    COMPANY = (
        (0,'Company Representative'),
        (1,'Individual'),
    )
    ROLE = (
        (0,'Talent'),
        (1,'Beta-Tester'),
        (2,'Industry Insider'),
    )
    PAID_TYPE = (
        (0,'Free'),
        (1,'Monthly'),
        (2,'Six-Monthly'),
        (3,'Twelve-Monthly'),
    )
    subscription = models.IntegerField(choices=PKG, default=0)
    middle_name = models.CharField(max_length=60, null=True, blank=True)
    synonym = models.CharField(max_length=15, null=True)
    permission = models.IntegerField(choices=COMPANY, default=1)
    role = models.IntegerField(choices=ROLE, default=0)
    paid = models.BooleanField(default=False, blank=True)
    paid_date = models.DateTimeField(null=True, blank=True)
    paid_type = models.IntegerField(choices=PAID_TYPE, default=0)

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class CustomUserSettings(models.Model):
    talent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    right_to_say_no = models.BooleanField('The right to say no to the sale of personal information', default=False)
    unsubscribe = models.BooleanField('Unsubscribe from all newsletters', default=False)
    receive_newsletter = models.BooleanField('Receive the newslatter', default=True)
    validation_requests = models.BooleanField('Receive validation requests', default=True)
    takeout = models.BooleanField('Export data to a csv file', default=False)
    right_to_be_forgotten = models.BooleanField('RIght to be forgotten', default=False)
