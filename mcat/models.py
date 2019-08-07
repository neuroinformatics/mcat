'''
MCAT Meeting Coordination Assistance Tool for Django
'''
__author__ = "Takayuki Kannon <kannon@brain.riken.jp>"

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from mcat import settings


TIME_SLOT_CHOICES = (
     ('day_full', _('Daily')),
     ('day_half', _('Half-daily')),
     ('hour_full', _('Hourly')),
)

OPTION_MODE_CHOICES = (
     ('none', _('No option')),
     ('web', _('Allow \"web\" option')),
     ('maybe', _('Allow \"maybe\" option')),
)

TIME_START_CHOICES = []
for t in range(0,24):
    TIME_START_CHOICES.append( ( str(t) , str(t)+':00' ) )
TIME_START_CHOICES = tuple(TIME_START_CHOICES)

TIME_END_CHOICES = []
for t in range(1,25):
    TIME_END_CHOICES.append( ( str(t) , str(t)+':00' ) )
TIME_END_CHOICES = tuple(TIME_END_CHOICES)

class Meeting(models.Model):
    user = models.ForeignKey(User)
    code = models.CharField(_("Meeting Code"), max_length=settings.code_length, primary_key=True)
    view_key = models.CharField(_("View Key"), max_length=settings.code_length)
    title = models.CharField(_("Title"), max_length=255)
    place = models.CharField(_("Place"), max_length=255)
    time_slot = models.CharField(_("Time slot"), max_length=9, choices=TIME_SLOT_CHOICES, default='hour_full')
    option_mode = models.CharField(_("Options"), max_length=5, choices=OPTION_MODE_CHOICES, default='none')
    remarks = models.TextField(_("Remarks"), blank=True)
    date_start = models.DateField(_("Candidate dates"))
    date_end = models.DateField(_("Candidate dates"))
    time_start = models.TextField(_("Time range"), max_length=2,choices=TIME_START_CHOICES, default='10')
    time_end = models.TextField(_("Time range"), max_length=2,choices=TIME_END_CHOICES, default='17')
    date_available = models.TextField()

    def __unicode__(self):
        return u'%s %s %s - %s' % (self.title, self.place, self.date_start, self.date_end)

    class Meta:
        verbose_name = _('Meeting')
        verbose_name_plural = _('Meetings')

class Attend(models.Model):
    code = models.ForeignKey(Meeting)
    name = models.CharField(_("Name"), max_length=255)
    mail = models.EmailField(_("E-mail"))
    comment = models.TextField(_("Comments"), blank=True)
    date_attend = models.TextField()
    update_key = models.CharField(_("Update Key"), max_length=settings.code_length)

    class Meta:
        unique_together = (("code", "mail"), ("code", "update_key"))
        verbose_name = _('Attend')
        verbose_name_plural = _('Attends')

    def __unicode__(self):
        return u'%s %s <%s>' % (self.code.title, self.name, self.mail)    
