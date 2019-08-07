'''
MCAT Meeting Coordination Assistance Tool for Django
'''
__author__ = "Takayuki Kannon <kannon@brain.riken.jp>"

from django.conf.urls import patterns, url

from mcat import settings

urlpatterns = patterns('mcat.views',
    url(r'^$', 'index'),
    url(r'^create/?$', 'create'),
    url(r'^create/detail/?$', 'create_detail'),
    url(r'^view/?$', 'view_index'),
    url(r'^view/(?P<code>' + settings.code_regex + ')/(?P<key>' + settings.code_regex + ')/$', 'view'),
    url(r'^delete/?$', 'delete'),
    url(r'^delete/(?P<code>' + settings.code_regex + ')/(?P<key>' + settings.code_regex + ')/$', 'delete_confirm'),
    url(r'^entry/?$', 'entry_index'),
    url(r'^entry/(?P<code>' + settings.code_regex + ')/$', 'entry'),
    url(r'^entry/(?P<code>' + settings.code_regex + ')/(?P<key>' + settings.code_regex + ')/$', 'update'),
)
