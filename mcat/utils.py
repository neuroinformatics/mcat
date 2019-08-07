'''
MCAT Meeting Coordination Assistance Tool for Django
'''
__author__ = "Takayuki Kannon <kannon@brain.riken.jp>"

import re
import datetime
import hashlib
from django.utils.translation import ugettext as _
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.contrib.sites.models import get_current_site
from mcat.models import Meeting, Attend
from mcat.forms import MeetingForm, MeetingDetailForm, EntryForm, DeleteForm
from mcat import settings

def validate_date_range(data):
    return bool(data['date_start'] <= data['date_end'])

def validate_time_range(data):
    return not bool(data['time_slot'] == "hour_full" and (int(data['time_start']) > int(data['time_end'])))

def validate_code(code):
    return bool(re.search(settings.code_validation_regex, code))

def generate_code():
    code = hashlib.sha256(datetime.datetime.now().isoformat()).hexdigest()[:int(settings.code_length)]
    return code

def render_index(request):
    template_file = 'index.html'
    template_assign = ({
        'navimode'  : "top",
        'site_name' : get_current_site(request).name,
    })
    return render_to_response(template_file, template_assign, context_instance=RequestContext(request))

def render_view_index(request, meetings=None, error=None):
    detailform = MeetingDetailForm()
    template_file = 'view_index.html'
    template_assign = ({
        'navimode'   : "view",
        'site_name'  : get_current_site(request).name,
        'meetings'   : meetings,
        'detailform' : detailform,
        'error'      : error,
    })
    return render_to_response(template_file,template_assign, context_instance=RequestContext(request))

def render_view(request, meeting):
    detailform = MeetingDetailForm(instance=meeting)
    attends = Attend.objects.filter(code=meeting)
    entryform = EntryForm()
    
    date_start = meeting.date_start
    date_end   = meeting.date_end
    time_start = int(meeting.time_start)
    time_end   = int(meeting.time_end)
    
    if meeting.time_slot == 'day_full' :
        cols = 1
        table_header_times = [_("All Day")]
    elif meeting.time_slot == 'day_half':
        cols = 2
        table_header_times = [_("AM"), _("PM")]
    else: # hour_full
        cols = time_end - time_start + 1
        table_header_times = [ (str(time_start+col)+":00") for col in range(0,cols) ]

    rows = (date_end - date_start).days + 1
    table_header_days = [ (date_start+datetime.timedelta(days=row)) for row in range(0,rows) ]

    aggregate_attend = [0] * rows*cols
    aggregate_option = [0] * rows*cols
    for attend in attends:
        for ind in range(0, rows*cols):
            if attend.date_attend[ind] == '1':
                aggregate_attend[ind] += 1
                aggregate_option[ind] += 1
            elif attend.date_attend[ind] == '2':
                aggregate_option[ind] += 1

    aggregate_attend_max = max(aggregate_attend)
    aggregate_option_max = max(aggregate_option)

    template_file = 'view.html'
    template_assign = ({
        'navimode'             : "view",
        'site_name'            : get_current_site(request).name,
        'meeting'              : meeting,
        'detailform'           : detailform,
        'attends'              : attends,
        'entryform'            : entryform,
        'entry_url'            : request.build_absolute_uri(reverse('mcat.views.entry', kwargs={'code':meeting.code})),
        'table_header_times'   : table_header_times,
        'table_header_days'    : table_header_days,
        'aggregate_attend'     : aggregate_attend,
        'aggregate_option'     : aggregate_option,
        'aggregate_attend_max' : aggregate_attend_max,
        'aggregate_option_max' : aggregate_option_max,
    })
    return render_to_response(template_file, template_assign, context_instance=RequestContext(request))

def render_delete_confirm(request, meeting = None, error = None):

    if meeting <> None:
        detailform = MeetingDetailForm(instance=meeting)
        deleteform = DeleteForm({'code':meeting.code,
                                 'view_key':meeting.view_key})
    else:
        detailform = MeetingDetailForm()
        deleteform = DeleteForm()
        
    template_file = 'delete.html'
    template_assign = ({
        'navimode'   : "view",
        'site_name'  : get_current_site(request).name,
        'meeting'    : meeting,
        'detailform' : detailform,
        'deleteform' : deleteform,
        'error'      : error,
    })
    return render_to_response(template_file, template_assign, context_instance=RequestContext(request))

def render_entry_index(request, error=None):
    template_file = 'entry_index.html'
    template_assign = ({
        'navimode'  : "entry",
        'site_name' : get_current_site(request).name,
        'error'     : error,
    })
    return render_to_response(template_file, template_assign, context_instance=RequestContext(request))

def render_entry(request, code, key, meeting, entryform):
    detailform = MeetingDetailForm(instance=meeting)

    date_start = meeting.date_start
    date_end   = meeting.date_end
    time_start = int(meeting.time_start)
    time_end   = int(meeting.time_end)
    
    if meeting.time_slot == 'day_full' :
        table_header_times = [_("All Day")]
    elif meeting.time_slot == 'day_half':
        table_header_times = [_("AM"), _("PM")]
    else: # hour_full
        table_header_times = [ (str(time_start+col)+":00") for col in range(0,time_end - time_start + 1) ]
    
    table_header_days = [ (date_start+datetime.timedelta(days=row)) for row in range(0,(date_end - date_start).days + 1) ]

    template_file = 'entry.html'
    template_assign = ({
        'navimode'           : "entry",
        'site_name'          : get_current_site(request).name,
        'code'               : code,
        'key'                : key,
        'entryform'           : entryform,
        'meeting'            : meeting,
        'detailform'         : detailform,
        'table_header_times' : table_header_times,
        'table_header_days'  : table_header_days,
    })
    return render_to_response(template_file, template_assign, context_instance=RequestContext(request))

def send_entry_mail(request,meeting,attend):
    entryform = EntryForm(request.POST)
    if entryform.is_valid():
        meetingform = MeetingForm(instance=meeting)
        subject = get_current_site(request).name + " " + _("registered the schedule") + " " + _(":") + " " + meeting.title
        message_template = get_template("entry.txt")
        message_context = Context({
               'site_name'   : get_current_site(request).name,
               'entryform'    : entryform,
               'meetingform' : meetingform,
               'admin_mail'  : settings.admin_mail,
               'update_url'  : request.build_absolute_uri(reverse('mcat.views.update', kwargs={'code':meeting.code, 'key':attend.update_key})),
        })
        message = message_template.render(message_context)
        send_mail(subject, message, settings.admin_mail, [ attend.mail ])

        subject = get_current_site(request).name + " " + _("registered the schedule") + " " + _(":") + " " + meeting.title + " " + attend.name
        message_template = get_template("entry_alert.txt")
        message_context = Context({
               'site_name'   : get_current_site(request).name,
               'entryform'    : entryform,
               'meetingform' : meetingform,
               'admin_mail'  : settings.admin_mail,
        })
        message = message_template.render(message_context)
        send_mail(subject, message, settings.admin_mail, [ meeting.user.email ])

def render_create(request, createform, date_range_error=False, time_range_error=False):
    template_file = 'create.html'
    template_assign = ({
        'navimode'         : "create",
        'site_name'        : get_current_site(request).name,
        'createform'       : createform,
        'date_range_error' : date_range_error,
        'time_range_error' : time_range_error,
    })
    return render_to_response(template_file, template_assign, context_instance=RequestContext(request))

def render_create_detail(request, createform, detailform):
    date_start = createform.cleaned_data['date_start']
    date_end   = createform.cleaned_data['date_end']
    time_start = int(createform.cleaned_data['time_start'])
    time_end   = int(createform.cleaned_data['time_end'])
    
    if createform.cleaned_data['time_slot'] == 'day_full' :
        table_header_times = [_("All Day")]
    elif createform.cleaned_data['time_slot'] == 'day_half':
        table_header_times = [_("AM"), _("PM")]
    else: # hour_full
        table_header_times = [ (str(time_start+col)+":00") for col in range(0,time_end - time_start + 1) ]
    
    table_header_days = [ (date_start+datetime.timedelta(days=row)) for row in range(0,(date_end - date_start).days + 1) ]

    template_file = 'create_detail.html'
    template_assign = ({
        'navimode'           : "create",
        'site_name'          : get_current_site(request).name,
        'createform'         : createform,
        'detailform'         : detailform,
        'table_header_times' : table_header_times,
        'table_header_days'  : table_header_days,
    })
    return render_to_response(template_file, template_assign, context_instance=RequestContext(request))

def send_create_mail(request, meeting):
    createform = MeetingForm(request.POST)
    detailform = MeetingDetailForm(request.POST)
    if createform.is_valid() and detailform.is_valid():
        subject = get_current_site(request).name + " " + _("created the meeting") + " " + _(":") + " " + meeting.title
        message_template = get_template("create.txt")
        message_context = Context({
               'site_name'  : get_current_site(request).name,
               'createform' : createform,
               'detailform' : detailform,
               'view_url'   : request.build_absolute_uri(reverse('mcat.views.view', kwargs={'code':meeting.code,'key':meeting.view_key})),
               'entry_url'   : request.build_absolute_uri(reverse('mcat.views.entry', kwargs={'code':meeting.code})),
        })
        message = message_template.render(message_context)
        send_mail(subject, message, settings.admin_mail, [ meeting.user.email ])
