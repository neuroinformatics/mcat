'''
MCAT Meeting Coordination Assistance Tool for Django
'''
__author__ = "Takayuki Kannon <kannon@brain.riken.jp>"

from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.views.generic.base import RedirectView
from mcatdjango import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^login/$', 'mcatdjango.views.login', name='login'),
    url(r'^update_profile/$', 'mcatdjango.views.update_profile'),

    # For User Registration
#     url(r'^registration/activate/(?P<activation_key>\w+)/$',
#        'registration.views.activate',
#        name='registration_activate'),
#     url(r'^registration/register/$',
#        'registration.views.register',
#        name='registration_register'),
#     url(r'^registration/register/complete/$',
#         direct_to_template,
#         {'template': 'registration/registration_complete.html'},
#         name='registration_complete'),
    ######################

    # For User Authentication
    url(r'^logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': settings.URL_ROOT + '/' },
        name='logout'),
    url(r'^auth/password_reset/$',
        'django.contrib.auth.views.password_reset',
        {'template_name': 'auth/password_reset_form.html', 'email_template_name': 'auth/password_reset_email.txt'},
        name='password_reset'),
    url(r'^auth/password_reset_done/$',
        'django.contrib.auth.views.password_reset_done',
        {'template_name': 'auth/password_reset_done.html'},
        name='password_reset_done'),
    url(r'^auth/password_reset_confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'template_name': 'auth/password_reset_confirm.html'},
        name='password_reset_confirm'),
    url(r'^auth/password_reset_complete/$',
        'django.contrib.auth.views.password_reset_complete',
        {'template_name': 'auth/password_reset_complete.html'},
        name='password_reset_complete'),
    ######################

    # Uncomment the next line for Shibboleth Authentication
    #url(r'^shibboleth/', include('django_shibboleth.urls')),

    # Uncomment the next line for Open ID authentification
    #url(r'^openid/', include('django_openid_auth.urls')),

#     url(r'^$', redirect_to, {'url': settings.URL_ROOT + '/mcat'}),
    url(r'^$', RedirectView.as_view(url= settings.URL_ROOT + '/mcat')),
    url(r'^mcat/', include('mcat.urls')),

)
