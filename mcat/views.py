'''
MCAT Meeting Coordination Assistance Tool for Django
'''
__author__ = "Takayuki Kannon <kannon@brain.riken.jp>"

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _

from mcat import utils, settings
from mcat.forms import MeetingForm, MeetingDetailForm, EntryForm, DeleteForm
from mcat.models import Meeting, Attend
from mcatdjango.views import post_login_check


def index(request):
    return utils.render_index(request)

@login_required
@post_login_check
def create(request):
    date_range_error = False
    time_range_error = False
    if request.method == 'POST':
        createform = MeetingForm(request.POST)

        if createform.is_valid():
            data = createform.cleaned_data

            if utils.validate_date_range(data) and utils.validate_time_range(data) :
                detailform = MeetingDetailForm(data)
                return utils.render_create_detail(request, createform, detailform)

        if not utils.validate_date_range(request.POST) :
            date_range_error = True

        if not utils.validate_time_range(request.POST) :
            time_range_error = True

    else:
        createform = MeetingForm()

    return utils.render_create(request, createform, date_range_error, time_range_error)

@login_required
@post_login_check
def create_detail(request):
    if request.method == 'POST':
        createform = MeetingForm(request.POST)
        detailform = MeetingDetailForm(request.POST)
        if createform.is_valid() and detailform.is_valid():
            data = detailform.cleaned_data
            meeting = Meeting(**data)
            meeting.user = request.user
            meeting.code = utils.generate_code()
            meeting.view_key = utils.generate_code()
            meeting.save()
            
            utils.send_create_mail(request, meeting)

            return HttpResponseRedirect(reverse('mcat.views.index'))

        data = createform.cleaned_data
        detailform = MeetingDetailForm(data)
        return utils.render_create_detail(request, createform, detailform)
    return HttpResponseRedirect(reverse('mcat.views.create'))

def view(request, code, key):
    try:
        meeting = Meeting.objects.get(pk=code)
    except Meeting.DoesNotExist:
        return utils.render_view_index(request, error=_("Meeting code doesn't exist!"))

    if meeting.view_key == key:
        return utils.render_view(request, meeting)
    else:
        return utils.render_view_index(request, error=_("View key doesn't match!"))

@login_required
def view_index(request):
    meetings = Meeting.objects.filter(user__exact=request.user)
    return utils.render_view_index(request, meetings)

@login_required
def delete(request):
    if request.method == 'POST':
        deleteform = DeleteForm(request.POST)
        if deleteform.is_valid():
            code = deleteform.cleaned_data['code']
            try:
                Meeting.objects.get(pk=code).delete()
            except Meeting.DoesNotExist:
                return utils.render_delete_confirm(request, error=_("Meeting code doesn't exist!"))
        else:
            return utils.render_delete_confirm(request, error=_("Illegal or malformed form data!"))        

    return HttpResponseRedirect(reverse('mcat.views.view_index'))

@login_required
def delete_confirm(request, code, key):
    try:
        meeting = Meeting.objects.get(pk=code)
    except Meeting.DoesNotExist:
        return utils.render_delete_confirm(request, error=_("Meeting code doesn't exist!"))

    if meeting.user <> request.user:
        return utils.render_delete_confirm(request, error=_("Operation not permitted!"))

    if meeting.view_key <> key:
        return utils.render_delete_confirm(request, error=_("View key doesn't match!"))

    return utils.render_delete_confirm(request, meeting=meeting)


def entry_index(request):
    return utils.render_entry_index(request)

def entry(request,code):
    try:
        meeting = Meeting.objects.get(pk=code)
    except Meeting.DoesNotExist:
        return utils.render_entry_index(request, error=_("Meeting code doesn't exist!"))

    if request.method == 'POST':
        entryform = EntryForm(request.POST)
        if entryform.is_valid():
            data = entryform.cleaned_data
            try:
                attend = Attend.objects.get(code=meeting, mail=data['mail'])
                attend.name = data['name']
                attend.comment = data['comment']
                attend.date_attend = data['date_attend']
            except Attend.DoesNotExist:
                attend = Attend(**data)
                attend.code = meeting
                attend.update_key = utils.generate_code()

            utils.send_entry_mail(request, meeting, attend)

            attend.save()
            return HttpResponseRedirect(reverse('mcat.views.index'))
    else:
        entryform = EntryForm()

    return utils.render_entry(request=request, code=code, key=None, meeting=meeting, entryform=entryform)

def update(request, code, key):

    try:
        meeting = Meeting.objects.get(pk=code)
    except Meeting.DoesNotExist:
        return utils.render_entry_index(request, error=_("Meeting code doesn't exist!"))

    try:
        attend = Attend.objects.get(update_key=key)
    except Attend.DoesNotExist:
        return utils.render_entry_index(request, error=_("Update key doesn't match!"))

    if request.method == 'POST':
        entryform = EntryForm(request.POST)
        if entryform.is_valid():
            data = entryform.cleaned_data
            attend.name = data['name']
            attend.mail = data['mail']
            attend.comment = data['comment']
            attend.date_attend = data['date_attend']
            attend.save()

            utils.send_entry_mail(request, meeting, attend)

            return HttpResponseRedirect(reverse('mcat.views.index'))
    else:
        entryform = EntryForm(instance=attend)

    return utils.render_entry(request=request, code=code, key=key, meeting=meeting, entryform=entryform)
