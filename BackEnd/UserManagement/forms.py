from django import forms
from django.contrib.auth.models import User
from UserManagement.models import *


from bson import Binary, Code
from bson.json_util import dumps
from bson.json_util import loads
import json
import os
from UserManagement.views import *


from django.template import RequestContext



############### REGISTRO DE USUARIOS #################
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('dni',)
