from django.contrib.auth.models import User, Permission, Group, AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _


class Person(AbstractUser):
    """Any user that can log in to BOZPlanner"""
    organizations = models.ManyToManyField("Organization", blank=True)
    agenda_token = models.CharField(max_length=64, editable=False, null=True)

    @property
    def is_admin(self):
        return self.groups.filter(name="Administrator").exists()

    @property
    def is_planner(self):
        return self.groups.filter(name="Planner").exists()

    @property
    def is_secretary(self):
        return self.groups.filter(name="Secretary").exists()
    
    @property
    def is_approver(self):
        return self.groups.filter(name="Approver").exists()
    
    @property
    def is_user_manager(self):
        return self.groups.filter(name="User Manager").exists()

    @property
    def all_organizations(self):
        result = []

        for organization in self.organizations.all():
            result += organization.all_organizations()

        return result

    def save(self, *args, **kwargs):
        if self.agenda_token is None:
            self.agenda_token = get_random_string(64, "0123456789abcdef")

        super(Person, self).save(*args, **kwargs)

    @staticmethod
    def validate_username(value):
        error = ValidationError(_('%(value)s is not a valid student number or employee number'),
            params={'value': value})

        if len(value) != 8:
            raise error

        if value[0] not in ['m', 's']:
            raise error

        if any(c not in "0123456789" for c in value[1:8]):
            raise error

    class Meta:
        verbose_name = "person"
        permissions = [
            ("change_groups", "Can change user groups"),
            ("list_persons", "Can view persons"),
        ]

    def __str__(self):
        return self.get_full_name()

Person._meta.get_field('username').help_text = 'The student number or employee number of the user, for example s1234567 or m1234567'
Person._meta.get_field('username').validators.append(Person.validate_username)
Person._meta.get_field('groups').help_text = ''

class Organization(models.Model):
    """An organization for which OLC meetings can be planned in BOZPlanner"""
    name = models.CharField(max_length=255)
    parent_organization = models.ForeignKey("Organization", null=True, blank=True,
        help_text="The organization to which this organization belongs. For example, Technical Computer Science might "
        "belong to an organization called EWI.")

    def all_organizations(self):
        result = [self]

        for organization in Organization.objects.filter(parent_organization=self):
            result += organization.all_organizations()

        return result

    def __str__(self):
        return self.name

class Preferences(models.Model):
    person = models.OneToOneField("Person")
    overview = models.ManyToManyField(Organization, blank=True, related_name='pref_overview')
    reminder = models.ManyToManyField(Organization, blank=True, related_name='pref_reminder')

    agenda_secretary = models.BooleanField(default=True,
        verbose_name="Include meetings in your agenda of which you are the secretary")
    agenda_organization = models.BooleanField(default=False,
        verbose_name="Include meetings in your agenda which belong to your organizations")
    overview_student = models.ManyToManyField(Organization, blank=True, related_name='student_pref_overview')
    confirmation_student = models.BooleanField(default=False,
        verbose_name="Receive confirmation mail when adding yourself to a meeting")

    zoom_in = models.BooleanField(default=False,
        verbose_name="Always zoom in the page")

    class Meta:
        verbose_name_plural = 'Preferences'
        verbose_name = 'Preferences'

    def __str__(self):
        return self._meta.verbose_name + ' for ' + self.person.__str__()


@receiver(post_save, sender=Person)
def create_preferences(sender, instance, created, **kwargs):
     if created:
         Preferences.objects.create(person=instance)
