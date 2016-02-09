from django.db import models

# Create your models here.
class User(models.Model):
    identifier = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    organization = models.ManyToManyField(Organization)

class Meeting(models.Model):
    place = models.CharField(max_length=255)
    date = models.DateField()
    begin_time = models.TimeField()
    end_time = models.TimeField()
    secretary = models.ForeignKey(User)
    organization = models.ForeignKey(Organization)

class Minutes(models.Model):
    meeting = models.ForeignKey(Meeting)

class Organization(models.Model):
    name = models.CharField(max_length=255)

# class Role(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()