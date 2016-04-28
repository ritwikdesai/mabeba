from django.shortcuts import render
from app.forms import Register, Login , Email, QRVerify
from app.api.qr import render as qr_render
from app.api import db
from app.api import crypto
import json
from django.http import HttpResponse,JsonResponse,Http404
from django.views.decorators.csrf import csrf_exempt
import uuid
#from django.core.mail import send_mail
from DjangoWebProject.settings import SECRET_KEY
# Create your views here.

DOMAIN = "meba.azurewebsites.net"
PRODUCTION_URL = 'https://meba.azurewebsites.net'

def do_register(request):
    form = Register()
    return render(request,'app/register.html',{'register_form':form})

def set_browser_session(request):
    if not request.session.exists(request.session.session_key):
        print "Creating Session"
        request.session.create()
        # request.session.set_expiry(60)

def register(request):
    #insert cookie logic for persistence
    set_browser_session(request)
    if request.method == "POST":
        form = Register(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            if db.no_user(data['username'],data['email_address']):
                #pr,pu = crypto.gen_key_pair()
                passwd = str(data['password'])
                key = crypto.key_from_pass(passwd,crypto.gen_salt(),crypto.ITER_100K,crypto.KEY_256)
                o = dict(data)
                o['secret'] = key
                o['otp_salt'] = crypto.gen_otp_secret()
                db.save_user(o)

                store = dict()
                store['site'] = "MABEBA Website"
                store['username'] = str(data['username'])
                store['token_url'] = PRODUCTION_URL + '/token/'
                store['secret'] = key
                store['otp_salt'] = o['otp_salt']

                salt = crypto.gen_salt()


                key = crypto.key_from_pass(passwd,salt,crypto.ITER_100K,crypto.KEY_256)
                key = crypto.key_to_bytes(key)

                encrypted = crypto.aes_encrypt(str(store),key)

                random_id = crypto.get_random_id()
                db.store_in_file(encrypted,random_id)

                o = dict()
                o['salt'] = salt
                o['token'] = PRODUCTION_URL + '/register/token/' + random_id
                o = json.dumps(o)
                print o

                data = qr_render(o)

                return render(request,'app/qr.html',{'data':data})

            else:
                return do_register(request)

        else:
            return do_register(request)


    else:
        return do_register(request)



def login(request):
    return index(request)

def do_login_get(request,msg=""):
    form = Login()
    resp = render(request,'app/login.html',{'login_form':form,'msg':msg})
    return resp

def do_login_post(request):
    form = Login(request.POST)
    if not form.is_valid():
        return do_login_get(request,"Invalid form entry")

    data = form.cleaned_data
    username = str(data['username'])
    password = str(data['password'])
    #otp = str(data['random_pass'])
    token = request.POST.get('token')

    if db.validate_login(request,username,password,token):
        #return HttpResponse(str({"id":"login","status":"success","msg":"Welcome " + username}))
        return render(request,'app/user_page.html',{'msg':'Welcome ' + str(username)})
    else:
        return do_login_get(request,"Invalid login details")



def index(request):
    set_browser_session(request)
    if request.method == "GET":
        return do_login_get(request)

    elif request.method == "POST":
        token = request.POST.get('token')
        if 'token' != "":
            return do_login_post(request)
        else:
            return do_login_get(request,"Please request a token first")

def qr(request):
    # send_mail('Subject here', 'Here is the message.', 'ritwikdesai@icloud.com',
    # ['desairitwik@gmail.com'], fail_silently=False)

    random_id = crypto.get_random_id()
    o = dict()
    import bcrypt
    o['salt'] = bcrypt.gensalt()
    o['token'] = PRODUCTION_URL + '/register/token/' + str(uuid.uuid4())
    o = json.dumps(o)
    print o

    data = qr_render(o)
    return render(request,'app/qr.html',{'data':data})

@csrf_exempt
def cookie_test(request):
    # o = request.COOKIES['login_cookie']
    # decrypted = crypto.decrypt(o,crypto.PRIVATE_KEY)
    print request.COOKIES

    print request.method
    decrypted = "helloWorld"
    resp = JsonResponse({})
    resp.set_cookie("tempcokie","fdgfdgfdg",httponly=True,secure=True,max_age=30);
    return resp


def to_cookie_str(session):
    o = dict()
    # o['user_id'] = session.user()
    # o['session_id'] = session.id()
    # o['random_nonce'] = session.nonce()
    # o['expiry_time'] = session.expiry()
    # o['other_data'] = session.extraData()
    o['user_id'] = session.user()
    o['expiry_time'] = session.expiry()
    data_to_be_secured = dict()
    data_to_be_secured['session_id'] = session.id()
    data_to_be_secured['random_nonce'] = session.nonce()
    data_to_be_secured['other_data'] = session.extraData()
    data_to_be_secured = json.dumps(data_to_be_secured)
    secure_key = crypto.sign_msg(SECRET_KEY,str(session.user()) + str(session.expiry()))
    secured_data = crypto.aes_encrypt(data_to_be_secured,secure_key,256)
    o['data'] = secured_data
    o['sign'] = crypto.sign_msg(secure_key,str(session.user())+str(session.expiry()) + data_to_be_secured)
    return json.dumps(o)

def test(request):
    o = json.loads('{"expiry_time": 1457600883, "sign": "434e2a769fa4ec350908b3f6ff7ddb2b2a435064886d9ab1d883719d94a9f5fd", "user_id": "geekyrvd", "data": "NiAawMEvqqvVzaJTY1ihc+oHHExvjgQvGqldSV01IJNoTu2OcL17Xv7uimYi4ymbEP6gMl4yQZf+NQsmJZyu/qE5MM//1rcMeiVOx/BbLlVXYpAn4XVd/qRI2zyirXyHgQdZ9QYiU8dNkAWtxQ1MjnnKeDg4JyUQu96RDVgPhIw="}');
    secret_key = crypto.sign_msg(SECRET_KEY , str(o['user_id']) + str(o['expiry_time']))
    data = crypto.aes_decrypt(str(o['data']),secret_key.encode(),256)
    match = str(o['sign']) == crypto.sign_msg(secret_key,str(o['user_id'])+str(o['expiry_time']) + data)

    print match
    return HttpResponse("Hello")

@csrf_exempt
def token_request(request):
    set_browser_session(request)
    msg = "Error"
    try:
        requestData = eval(request.body)
        user_id = requestData['username']
        timestamp = requestData['timestamp']
        session_data = requestData['data']
        session,msg = db.create_session(request.session.session_key,user_id,timestamp,session_data)

        if session.isValid():
            print "Valid Session found"
            value = db.create_token_str(session)
            resp = JsonResponse({"id":"responseToken","success":True,"data":"Success","domain":DOMAIN,"token":value})
            #resp.set_cookie('token',value,httponly=True,secure=True,max_age= 5 * 60,domain='iitr-semx.azurewebsites.net')
            return resp
    except Exception,e:
        print e

    return JsonResponse({"id":"responseToken","success":False,"data":msg})

def register_token(request,token_id):
    print token_id
    if db.file_exists(token_id):
        data = db.read_file(token_id)
        db.delete_file(token_id)

        o = dict()
        o['register'] = data

        return JsonResponse(o)

    return JsonResponse({})


def request_qr(request):
    return email_reset(request,'/request/qr/',False)

def email_reset(request,url,reset):

    if request.method == "GET":
        form = Email()
        return render(request,'app/request_qr.html',{'email_form':form,'action_str':url})

    else:
        form = Email(request.POST)
        msg = "Invalid Email Address"

        if not form.is_valid():
            return render(request,'app/message.html',{'msg':msg})

        data = form.cleaned_data

        if db.unique_user(data['username'],data['email_address']):
            o = db.save_qr_request(data['email_address'],reset)
            mail_msg = """
            <html>
            <head>
                <title> QR Request </title>
            </head>
            <body>
                <a href="%s">Click Here</a>
            </body>
            </html>
            """ % (PRODUCTION_URL + url +o.request_id)
            #send_mail('QR Request', mail_msg, 'semx@example.com',[data['email_address']], fail_silently=False)
            msg = "An Email has been sent to " + data['email_address']
            return render(request,'app/message.html',{'msg':msg})


def qr_request(request,qr_id):
    if request.method == "GET":
        if db.qr_request_exists(qr_id):
            form = QRVerify()
            return render(request,'app/qr_verify.html',{'qr_verify':form})
        else:
            return Http404("Not Found")
    else:
        form = QRVerify(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            o = db.get_user(data['username'],data['password'])
            if o is None:
                return render(request,'app/message.html',{"msg":'Invalid Login Details'})

            store = dict()
            store['site'] = "SemX Website"
            store['username'] = str(o.user_id)
            store['token_url'] = PRODUCTION_URL + '/token/'
            store['secret'] = str(o.secret)
            store['otp_salt'] = str(o.otp_salt)

            salt = crypto.gen_salt()

            key = crypto.key_from_pass(str(data['password']),salt,crypto.ITER_100K,crypto.KEY_256)
            key = crypto.key_to_bytes(key)

            encrypted = crypto.aes_encrypt(str(store),key)
            random_id = crypto.get_random_id()
            db.store_in_file(encrypted,random_id)

            o = dict()
            o['salt'] = salt
            o['token'] = PRODUCTION_URL + '/register/token/' + random_id
            o = json.dumps(o)

            resp = qr_render(o)

            return render(request,'app/qr.html',{'data':resp})


        return render(request,'app/message.html',{"msg":'Invalid Login Details'})


def secret_reset(request,request_id):
    if request.method == "GET":
        if db.qr_request_exists(request_id):
            form = QRVerify()
            return render(request,'app/qr_verify.html',{'qr_verify':form})
        else:
            return Http404("Not Found")
    else:
        form = QRVerify(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            o = db.get_user(data['username'],data['password'])
            if o is None:
                return render(request,'app/message.html',{"msg":'Invalid Login Details'})


            passwd = str(data['password'])
            key = crypto.key_from_pass(passwd,crypto.gen_salt(),crypto.ITER_100K,crypto.KEY_256)
            new_secret = key
            new_otp_salt = crypto.gen_otp_secret()
            o = db.update_user(o,secret=new_secret,otp_salt=new_otp_salt)

            store = dict()
            store['site'] = "SemX Website"
            store['username'] = str(o.user_id)
            store['token_url'] = PRODUCTION_URL + '/token/'
            store['secret'] = str(o.secret)
            store['otp_salt'] = str(o.otp_salt)

            salt = crypto.gen_salt()

            key = crypto.key_from_pass(str(data['password']),salt,crypto.ITER_100K,crypto.KEY_256)
            key = crypto.key_to_bytes(key)

            encrypted = crypto.aes_encrypt(str(store),key)
            random_id = crypto.get_random_id()
            db.store_in_file(encrypted,random_id)

            o = dict()
            o['salt'] = salt
            o['token'] = PRODUCTION_URL + '/register/token/' + random_id
            o = json.dumps(o)

            resp = qr_render(o)

            return render(request,'app/qr.html',{'data':resp})


        return render(request,'app/message.html',{"msg":'Invalid Login Details'})


def request_secret_reset(request):
    return email_reset(request,'/secret/reset/',True)
