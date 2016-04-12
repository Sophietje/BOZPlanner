from django.contrib.auth.models import User, Permission, Group, AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _


class Person(AbstractUser):
    """Any user that can log in to BOZPlanner"""
    organizations = models.ManyToManyField("Organization", verbose_name=_("organizations"), blank=True)
    calendar_token = models.CharField(max_length=64, verbose_name=_("calendar token"), editable=False, null=True)
    first_login = models.BooleanField(default=True, verbose_name=_("first login"))

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
    def is_user_manager(self):
        return self.groups.filter(name="User Manager").exists()

    @property
    def full_email(self):
        return '{} {} <{}>'.format(self.first_name, self.last_name, self.email)

    @property
    def all_organizations(self):
        result = set()

        for organization in self.organizations.all():
            result |= organization.all_organizations

        return list(result)

    def save(self, *args, **kwargs):
        if self.calendar_token is None:
            self.calendar_token = get_random_string(64, "0123456789abcdef")

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

Person._meta.get_field('username').help_text = _('The student number or employee number of the user, for example s1234567 or m1234567')
Person._meta.get_field('username').validators.append(Person.validate_username)
Person._meta.get_field('groups').help_text = ''
Person._meta.get_field('email').required = True


class Organization(models.Model):
    """An organization for which OLC meetings can be planned in BOZPlanner"""
    name = models.CharField(max_length=255, verbose_name=_("name"))
    parent_organization = models.ForeignKey("Organization", null=True, blank=True,
        verbose_name=_("parent organization"),
        help_text=_("The organization to which this organization belongs. For example, Technical Computer Science"
            " might belong to an organization called EWI."  ))

    @property
    def all_organizations(self):
        todo = {self}
        done = {self}

        while todo:
            org = todo.pop()

            for child in Organization.objects.filter(parent_organization=org):
                if child not in done:
                    todo.add(child)
                    done.add(child)

        return done

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "organization"
        permissions = [
            ("list_organizations", "Can list organizations"),
        ]

class Preferences(models.Model):
    person = models.OneToOneField("Person")
    overview = models.ManyToManyField(Organization, blank=True, related_name='pref_overview',
        verbose_name=_("overview"),
        help_text=_("You can use this to indicate of which organizations you would like to receive a weekly overview."))
    reminder = models.ManyToManyField(Organization, blank=True, related_name='pref_reminder',
        verbose_name=_("reminder"),
        help_text=_("You can use this to indicate of which organizations you would like to receive a reminder "
                    "whenever no secretary has been found 10 days in advance of a meeting."))

    calendar_secretary = models.BooleanField(default=True,
        verbose_name=_("Include meetings in your calendar of which you are the secretary"))
    calendar_organization = models.BooleanField(default=False,
        verbose_name=_("Include meetings in your calendar which belong to your organizations"))
    overview_secretary = models.ManyToManyField(Organization, verbose_name=_("overview secretary"), blank=True,
        related_name='student_pref_overview',
        help_text=_("You can use this to indicate of which organizations you would like to receive a weekly overview "
                    "of meetings that do not yet have a secretary."))
    confirmation_secretary = models.BooleanField(default=False,
        verbose_name=_("Receive confirmation mail when adding yourself to a meeting"),
        help_text=_("You can use this to indicate whether you would like to receive a confirmation mail whenever "
                    "you subscribe to or unsubscribe from a meeting."))

    zoom_in = models.BooleanField(default=False, verbose_name=_("Always zoom in the page"))

    class Meta:
        verbose_name_plural = 'Preferences'
        verbose_name = 'Preferences'

    def __str__(self):
        return self._meta.verbose_name + ' for ' + self.person.__str__()


@receiver(post_save, sender=Person)
def create_preferences(sender, instance, created, **kwargs):
     if created:
         Preferences.objects.create(person=instance)
