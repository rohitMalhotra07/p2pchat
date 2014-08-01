import re
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
CATEGORIES = (
    ('C1', 'IIT-B'),
    ('C2', 'IIT-K'),
    ('C3', 'IIT-KGP'),
    ('C4', 'IIT-M'),
)

class RegistrationForm(forms.Form):
 
    def __init__(self,*args,**kwargs):
        super(RegistrationForm,self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['onblur'] = "checkValidEmail();"
        self.fields['password2'].widget.attrs['onblur']="matchpassword();"

    name = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Name"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password (again)"))
    roll_no=forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=20)),label="Batch Id" )
    college_name = forms.ChoiceField(choices=CATEGORIES, required=True,label="College Name")

class LoginForm(forms.Form):
    email=forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Name"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    password=forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))

    