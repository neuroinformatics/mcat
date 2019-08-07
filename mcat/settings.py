'''
MCAT Meeting Coordination Assistance Tool for Django
'''
__author__ = "Takayuki Kannon <kannon@brain.riken.jp>"

from django.conf import settings


admin_mail = settings.SERVER_EMAIL

code_length = 16
code_regex = r'[A-Za-z0-9_]{'+str(code_length)+r'}'
code_validation_regex = r'^'+str(code_regex)+r'$'
