from app.models import Account,SessionData, RequestQR
from app.api import crypto
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import json
from DjangoWebProject.settings import SECRET_KEY
EXPIRY_OFFSET = 5
TOKEN_REQUEST_DIFF = 10

class Session:

    def __init__(self,session_id=None,user_id=None,random_nonce = None,expiry_time=None,other_data= None,is_valid=False):
        self.__session_id = session_id
        self.__user_id = user_id
        self.__random_nonce = random_nonce
        self.__expiry_time = expiry_time
        self.__other_data = other_data
        self.__is_valid = is_valid


    def id(self):
        return self.__session_id

    def isValid(self):
        if self.__user_id is None or self.__random_nonce is None or self.__expiry_time is None:
            return False
        return self.__is_valid

    def user(self):
        return self.__user_id

    def nonce(self):
        return self.__random_nonce

    def expiry(self):
        return self.__expiry_time

    def extraData(self):
        return self.__other_data

def create_session(session_id,user_id,timestamp,session_data):

    try:
        o = Account.objects.get(pk=user_id)
        key = crypto.sign_msg(str(o.secret),user_id+timestamp).digest()
        session_data = crypto.aes_decrypt(session_data,key)
        session_data = str(session_data).split(",")
        username = session_data[0]
        tstamp = int(session_data[1])
        if str(tstamp) != timestamp:
            return Session(is_valid=False),'invalid request'

        diff = int(crypto.now()) - tstamp

        if username == o.user_id and diff < TOKEN_REQUEST_DIFF:
            nonce = crypto.get_random_id()
            expiry = int(crypto.now()) + EXPIRY_OFFSET * 60
            other_data = None
            u = Session(session_id,user_id,nonce,expiry,other_data,True)
            save_session_data(u)
            return u,"success"
    except Account.DoesNotExist:
        return Session(is_valid = False),'username not found'

    return Session(is_valid = False),"token request timeout"


def no_user(username,email):
    try:
        o = Account.objects.raw("SELECT * FROM app_account WHERE user_id=%s OR email_address=%s",[username,email])
        if len(list(o)) == 0:
            return True
    except Account.DoesNotExist :
        return True
    return False

def get_user(username,password):
    try:
        o = Account.objects.get(user_id=username)
        passwd = crypto.secure_pw(password,o.passwd_salt)
        if passwd == o.password:
            return o
    except Account.DoesNotExist:
        return None

def unique_user(username,email):
    try:
        o = Account.objects.get(user_id=username,email_address=email)
        return True
    except Account.DoesNotExist:
        return False

def validate_login(request,username,passwd,token,otp=None):

    try:
        account = Account.objects.get(user_id=username)
        secure_pw = crypto.secure_pw(str(passwd),account.passwd_salt,fast=True)

        if secure_pw == account.password:
            # token_data = get_token_data(token)
            session_data = SessionData.objects.get(session_id=request.session.session_key)
            print session_data.user_id,session_data.random_nonce,session_data.session_id,session_data.expiry_time
            return validate_token(token,session_data)
    except (Account.DoesNotExist,SessionData.DoesNotExist):
        return False

    return False

def validate_token(token_data,session_data):
    try:
        token = json.loads(token_data)
        secret_key = crypto.sign_msg(SECRET_KEY , str(token['user_id']) + str(token['expiry_time'])).digest()
        data = crypto.aes_decrypt(str(token['data']),secret_key,256)
        if crypto.sign_msg(secret_key,str(token['user_id'])+str(token['expiry_time']) + data).hexdigest() != str(token['sign']):
            return False
        data = json.loads(data)
        if str(data['session_id']) == session_data.session_id and str(data['user_id']) == str(session_data.user_id) and str(data['random_nonce']) == session_data.random_nonce and str(data['other_data']) == str(session_data.other_data):
            print "Token Validated"
            return True
        else:
            return False

    except Exception,e:
        print e
        return False

    return False
    # #check expired
    # if token['expiry_time'] < crypto.now():
    #     return False
    #
    # if str(token['session_id']) == session_data.session_id and str(token['user_id']) == str(session_data.user_id) and str(token['random_nonce']) == session_data.random_nonce and str(token['other_data']) == str(session_data.other_data):
    #     print "Token Validated"
    #     return True
    #
    # return False

def save_user(user):
    o = Account()
    o.f_name = str(user['first_name'])
    o.l_name = str(user['last_name'])
    o.user_id = str(user['username'])
    o.email_address = str(user['email_address'])
    o.secret = str(user['secret'])
    o.otp_salt = str(user['otp_salt'])
    o.passwd_salt = str(crypto.gen_salt())
    o.password = crypto.secure_pw(str(user['password']),o.passwd_salt,fast=True)
    o.save()
    return o

def update_user(user,**kwargs):
    if 'f_name' in kwargs:
        user.f_name = str(kwargs.pop('f_name'))
    if 'l_name' in kwargs:
        user.l_name = str(kwargs.pop('l_name'))
    if 'email_address' in kwargs:
        user.email_address = str(kwargs.pop('email_address'))
    if 'secret' in kwargs:
        user.secret = str(kwargs.pop('secret'))
    if 'otp_salt' in kwargs:
        user.otp_salt = str(kwargs.pop('otp_salt'))
    if 'passwd_salt' in kwargs and 'password' in kwargs:
        user.passwd_salt = str(kwargs.pop('passwd_salt'))
        user.password = crypto.secure_pw(str(kwargs.pop('password')),user.passwd_salt,fast=True)
    user.save()
    return user

def save_session_data(session):
    o = None
    try:
        o = SessionData.objects.get(pk = session.id())
    except SessionData.DoesNotExist:
        o = SessionData()

    o.user_id = session.user()
    o.session_id = session.id()
    o.expiry_time = session.expiry()
    o.other_data = session.extraData()
    o.random_nonce = session.nonce()
    o.save()

def save_qr_request(email,reset=False):
    o = RequestQR()
    o.request_id = crypto.get_random_id()
    o.email_address = email
    o.reset = reset
    o.expiry_time = int(crypto.now()) + EXPIRY_OFFSET * 60
    o.save()
    return o

def qr_request_exists(qr_id):
    try:
        o = RequestQR.objects.get(request_id=qr_id)
        if o.expiry_time < int(crypto.now()):
            return False
        return True
    except RequestQR.DoesNotExist:
        return False

def store_in_file(data,file_name):
    default_storage.save(file_name,ContentFile(data))

def delete_file(file_name):
    default_storage.delete(file_name)

def read_file(file_name):
    return default_storage.open(file_name).read()

def file_exists(file_name):
    return default_storage.exists(file_name)


def get_token_data(data):
    # f = open('/Users/ritwikdesai/Developer/PythonEnv/lib/python2.7/site-packages/sslserver/certs/development.key')
    # key = f.read()
    # f.close()
    return crypto.decrypt(data,crypto.get_private_key())

def create_token_str(session):
    o = dict()
    o['user_id'] = session.user()
    o['expiry_time'] = session.expiry()
    data_to_be_secured = dict()
    data_to_be_secured['user_id'] = session.user()
    data_to_be_secured['session_id'] = session.id()
    data_to_be_secured['random_nonce'] = session.nonce()
    data_to_be_secured['other_data'] = session.extraData()
    data_to_be_secured = json.dumps(data_to_be_secured)
    secure_key = crypto.sign_msg(SECRET_KEY,str(session.user()) + str(session.expiry())).digest()
    secured_data = crypto.aes_encrypt(data_to_be_secured,secure_key,256)
    o['data'] = secured_data
    o['sign'] = crypto.sign_msg(secure_key,str(session.user())+str(session.expiry()) + data_to_be_secured).hexdigest()
    print o
    return json.dumps(o)
