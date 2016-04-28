"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))


class Register(forms.Form):
    email_address = forms.EmailField(label="",widget=forms.EmailInput(attrs={'placeholder':'Enter your email','required':'required'}),max_length=50)
    first_name = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'first name','required':'required'}),max_length=50)
    last_name = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'last name','required':'required'}),max_length= 50)
    username = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'username','required':'required'}))
    password = forms.CharField(label="",widget=forms.PasswordInput(attrs={'placeholder':'Enter your password','required':'required'}))
    match_pass = forms.CharField(label="",widget=forms.PasswordInput(attrs={'placeholder':'Re-enter your password','required':'required'}))

    def clean(self):
        cleaned_data = super(Register,self).clean()

        email = cleaned_data.get("email_address")
        f_name = cleaned_data.get("first_name")
        l_name = cleaned_data.get("last_name")
        u_name = cleaned_data.get("username")
        passwd = cleaned_data.get("password")
        m_pass = cleaned_data.get("match_pass")

        if '@' not in email:
            raise forms.ValidationError("Invalid Email Address entered")

        #Add logic to check username and email exists or not?

        if passwd != m_pass:
            raise forms.ValidationError("Passwords didn't match")

        return cleaned_data

class Login(forms.Form):
    username = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'Enter your Username','required':'required'}))
    password = forms.CharField(label="",widget=forms.PasswordInput(attrs={'placeholder':'Enter your password','required':'required'}))
    #random_pass = forms.IntegerField(label="",widget=forms.PasswordInput(attrs={'placeholder':'Enter 6-Digit OTP from your App','required':'required'}))

class Email(forms.Form):
    username = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'Enter your Username','required':'required'}))
    email_address = forms.EmailField(label="",widget=forms.EmailInput(attrs={'placeholder':'Enter your email','required':'required'}),max_length=50)

    def clean(self):
        cleaned_data = super(Email,self).clean()
        email = cleaned_data.get("email_address")

        if '@' not in email:
            raise forms.ValidationError("Invalid Email Address entered")

        return cleaned_data


class QRVerify(forms.Form):
    username = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'Enter your Username','required':'required'}))
    password = forms.CharField(label="",widget=forms.PasswordInput(attrs={'placeholder':'Enter your password','required':'required'}))
