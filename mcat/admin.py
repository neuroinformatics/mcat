'''
MCAT Meeting Coordination Assistance Tool for Django
'''
__author__ = "Takayuki Kannon <kannon@brain.riken.jp>"

from django.contrib import admin

from mcat.models import Attend, Meeting


admin.site.register(Meeting)
admin.site.register(Attend)
