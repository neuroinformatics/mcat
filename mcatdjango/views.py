'''
MCAT Meeting Coordination Assistance Tool for Django
'''
__author__ = "Takayuki Kannon <kannon@brain.riken.jp>"

from functools import wraps

from django.contrib.auth.views import login as auth_login
from django.contrib.auth.models import User
from django.contrib.sites.models import get_current_site
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.decorators import available_attrs
from django.utils.http import is_safe_url

from mcatdjango import settings
from mcatdjango.forms import PostLoginForm


def login(request):

    if 'USE_DJANGO_OPENID_AUTH' in vars(settings):
        use_django_openid_auth = vars(settings)['USE_DJANGO_OPENID_AUTH']
    else:
        use_django_openid_auth = False
        
    if 'USE_DJANGO_SHIBBOLETH' in vars(settings):
        use_django_shibboleth = vars(settings)['USE_DJANGO_SHIBBOLETH']
    else:
        use_django_shibboleth = False

    template_name = 'auth/login.html'
    extra_context = ({
        'navimode'                  : "login",
        'use_django_openid_auth'    : use_django_openid_auth,
        'use_django_shibboleth'     : use_django_shibboleth,
    })

    return auth_login(request,
                      template_name=template_name,
                      redirect_field_name='next',
                      extra_context=extra_context     
                      )

def post_login_check(func):
    '''
    Post login check decorator function
    if user is not authenticated, it'll be redirected to login page.
    if email is not set, it'll be redirected to profile edit page.
    
    '''
    @wraps(func,assigned=available_attrs(func))
    def __wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(settings.LOGIN_URL+'?next=%s' % request.path)

        if __actual_post_login_check(request):
            return func(request, *args, **kwargs)
        
        return HttpResponseRedirect(reverse(update_profile)+'?next=%s' % request.path)
    return __wrapped_view

def __actual_post_login_check(request):
    first_name = request.user.first_name
    last_name  = request.user.last_name
    email      = request.user.email
    try:
        validators.validate_email(email)
    except ValidationError:
        return False
    return True

def update_profile(request):
    next_page = None
    if 'next' in request.REQUEST:
        next_page = request.REQUEST['next']
        if not is_safe_url(url=next_page, host=request.get_host()):
            next_page = request.path

    if request.method == 'POST':
        updateprofileform = PostLoginForm(request.POST)
        if updateprofileform.is_valid():
            user = User.objects.get(username__exact=request.user.username)
            user.first_name = updateprofileform.cleaned_data['first_name']
            user.last_name  = updateprofileform.cleaned_data['last_name']
            user.email      = updateprofileform.cleaned_data['email']
            user.save()

            if next_page:
                return HttpResponseRedirect(next_page)
            return HttpResponseRedirect(settings.URL_ROOT)
    else:
        first_name = request.user.first_name
        last_name  = request.user.last_name
        email      = request.user.email
        updateprofileform = PostLoginForm({'first_name':first_name, 'last_name':last_name, 'email':email})

    template_file = 'auth/update_profile.html'
    template_assign = ({
        'navimode'          : "login",
        'site'              : get_current_site(request),
        'site_name'         : get_current_site(request).name,
        'updateprofileform' : updateprofileform,
        'next'              : next_page,
    })

    return render_to_response(template_file, template_assign, context_instance=RequestContext(request))
